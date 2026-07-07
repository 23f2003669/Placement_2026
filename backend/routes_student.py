from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User, Student, JobPosition, Application, Placement, Company
from decorators import role_required
from datetime import datetime
from cache import cache_get, cache_set
import json
from werkzeug.utils import secure_filename
import os

student_bp = Blueprint('student', __name__, url_prefix='/api/student')


def clear_student_cache(student_id):
    from cache import cache_delete
    cache_delete('available_jobs_raw')


@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('student')
def student_dashboard():
    """Student dashboard showing statistics."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        total_applications = Application.query.filter_by(student_id=student.id).count()
        shortlisted = Application.query.filter_by(student_id=student.id, status='shortlisted').count()
        selected = Application.query.filter_by(student_id=student.id, status='selected').count()
        total_placements = Placement.query.filter_by(student_id=student.id).count()

        return jsonify({
            'success': True,
            'data': {
                'student': {
                    'id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': User.query.get(student.user_id).email,
                    'roll_number': student.roll_number,
                    'branch': student.branch,
                    'year': student.year,
                    'cgpa': student.cgpa
                },
                'statistics': {
                    'total_applications': total_applications,
                    'shortlisted': shortlisted,
                    'selected': selected,
                    'total_placements': total_placements
                }
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/jobs', methods=['GET'])
@jwt_required()
@role_required('student')
def get_available_jobs():
    """
    Approved jobs the student can see, with per-student eligibility.
    Only the raw approved-job list is cached (5 min). Search and eligibility
    are computed fresh per request, so students never see each other's
    eligibility flags.
    """
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        raw_jobs = cache_get('available_jobs_raw')
        if raw_jobs is None:
            jobs = JobPosition.query.filter_by(status='approved').all()
            raw_jobs = []
            for job in jobs:
                company = Company.query.get(job.company_id)
                raw_jobs.append({
                    'id': job.id,
                    'job_title': job.job_title,
                    'job_description': job.job_description,
                    'company_name': company.company_name if company else None,
                    'company_id': job.company_id,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'location': job.location,
                    'min_cgpa': job.min_cgpa,
                    'eligible_branches': job.eligible_branches,
                    'eligible_years': job.eligible_years,
                    'application_deadline': job.application_deadline.isoformat()
                })
            cache_set('available_jobs_raw', raw_jobs, timeout=300)

        search_query = request.args.get('search', '').lower()
        if search_query:
            raw_jobs = [j for j in raw_jobs if
                        search_query in j['job_title'].lower() or
                        search_query in (j['job_description'] or '').lower()]

        job_list = []
        for j in raw_jobs:
            is_eligible = True
            reasons = []

            if j['min_cgpa'] and (student.cgpa is None or student.cgpa < j['min_cgpa']):
                is_eligible = False
                reasons.append(f"CGPA {student.cgpa} below required {j['min_cgpa']}")

            if j['eligible_branches']:
                branches = [b.strip().lower() for b in j['eligible_branches'].split(',')]
                if (student.branch or '').strip().lower() not in branches:
                    is_eligible = False
                    reasons.append(f"Branch {student.branch} not eligible")

            if j['eligible_years']:
                years = [int(y.strip()) for y in j['eligible_years'].split(',')]
                if student.year not in years:
                    is_eligible = False
                    reasons.append(f"Year {student.year} not eligible")

            item = dict(j)
            item.pop('job_description', None)
            item['is_eligible'] = is_eligible
            item['ineligibility_reasons'] = reasons if not is_eligible else []
            job_list.append(item)

        return jsonify({
            'success': True,
            'total': len(job_list),
            'jobs': job_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/apply-job/<int:job_id>', methods=['POST'])
@jwt_required()
@role_required('student')
def apply_for_job(job_id):
    """Student applies for a job. Checks eligibility and prevents duplicates."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        job = JobPosition.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404

        if job.status != 'approved':
            return jsonify({'error': 'This job is not available for applications'}), 400

        existing_application = Application.query.filter_by(
            student_id=student.id, job_position_id=job_id).first()
        if existing_application:
            return jsonify({'error': 'You have already applied for this job'}), 400

        if job.min_cgpa and (student.cgpa is None or student.cgpa < job.min_cgpa):
            return jsonify({'error': f'Your CGPA {student.cgpa} is below required {job.min_cgpa}'}), 400

        if job.eligible_branches:
            branches = [b.strip().lower() for b in job.eligible_branches.split(',')]
            if (student.branch or '').strip().lower() not in branches:
                return jsonify({'error': f'Your branch {student.branch} is not eligible'}), 400

        if job.eligible_years:
            years = [int(y.strip()) for y in job.eligible_years.split(',')]
            if student.year not in years:
                return jsonify({'error': f'Your year {student.year} is not eligible'}), 400

        application = Application(
            student_id=student.id,
            job_position_id=job_id,
            status='applied',
            applied_on=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()
        clear_student_cache(student.id)

        return jsonify({
            'success': True,
            'message': f'Successfully applied for {job.job_title}',
            'application': {
                'id': application.id,
                'job_id': job.id,
                'job_title': job.job_title,
                'status': application.status,
                'applied_on': application.applied_on.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@student_bp.route('/my-applications', methods=['GET'])
@jwt_required()
@role_required('student')
def get_student_applications():
    """Get all applications submitted by this student."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        applications = Application.query.filter_by(student_id=student.id).all()
        app_list = []
        for app in applications:
            job = JobPosition.query.get(app.job_position_id)
            company = Company.query.get(job.company_id)
            app_list.append({
                'application_id': app.id,
                'job_id': job.id,
                'job_title': job.job_title,
                'company_name': company.company_name if company else None,
                'status': app.status,
                'applied_on': app.applied_on.isoformat(),
                'shortlisted_on': app.shortlisted_on.isoformat() if app.shortlisted_on else None,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'company_feedback': app.company_feedback
            })

        return jsonify({'success': True, 'total': len(app_list), 'applications': app_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/placements', methods=['GET'])
@jwt_required()
@role_required('student')
def get_student_placements():
    """Get placement history for this student."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        placements = Placement.query.filter_by(student_id=student.id).all()
        placement_list = []
        for p in placements:
            company = Company.query.get(p.company_id)
            placement_list.append({
                'id': p.id,
                'company_name': company.company_name if company else None,
                'job_title': p.job_title,
                'salary': p.salary,
                'currency': p.currency,
                'joining_date': p.joining_date.isoformat() if p.joining_date else None,
                'status': p.status,
                'placed_on': p.placed_on.isoformat() if p.placed_on else None
            })

        return jsonify({'success': True, 'total': len(placement_list), 'placements': placement_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/export-applications', methods=['POST'])
@jwt_required()
@role_required('student')
def export_applications():
    """Student triggers CSV export of their applications (background task)."""
    try:
        from tasks import export_student_applications
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        task = export_student_applications.delay(student.id)
        return jsonify({
            'success': True,
            'message': 'Export started. You will receive your CSV shortly.',
            'task_id': task.id
        }), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/export-status/<task_id>', methods=['GET'])
@jwt_required()
@role_required('student')
def check_export_status(task_id):
    """Check status of export task."""
    try:
        from celery_config import celery_app
        task_result = celery_app.AsyncResult(task_id)

        if task_result.state == 'PENDING':
            return jsonify({'success': True, 'status': 'pending', 'message': 'Export is being processed...'}), 200
        elif task_result.state == 'SUCCESS':
            return jsonify({'success': True, 'status': 'completed', 'message': 'Export completed!', 'data': task_result.result}), 200
        elif task_result.state == 'FAILURE':
            return jsonify({'success': False, 'status': 'failed', 'error': str(task_result.info)}), 400
        else:
            return jsonify({'success': True, 'status': task_result.state.lower(), 'message': f'Export status: {task_result.state}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/upload-resume', methods=['POST'])
@jwt_required()
@role_required('student')
def upload_resume():
    """Upload student resume file."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        filename = secure_filename(f"{student.id}_{file.filename}")
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        student.resume_url = f"/uploads/resumes/{filename}"
        db.session.commit()

        return jsonify({'success': True, 'resume_url': student.resume_url, 'message': 'Resume uploaded successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@student_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required('student')
def get_profile():
    """Return the logged-in student's full profile."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        user = User.query.get(student.user_id)
        return jsonify({
            'success': True,
            'profile': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': user.email if user else None,
                'roll_number': student.roll_number,
                'phone': student.phone,
                'branch': student.branch,
                'year': student.year,
                'cgpa': student.cgpa,
                'bio': student.bio,
                'resume_url': student.resume_url
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required('student')
def update_profile():
    """Update editable fields of the logged-in student's profile."""
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        new_roll = data.get('roll_number')
        if new_roll and new_roll != student.roll_number:
            clash = Student.query.filter(
                Student.roll_number == new_roll,
                Student.id != student.id
            ).first()
            if clash:
                return jsonify({'error': 'Roll number already in use'}), 409
            student.roll_number = new_roll

        if 'cgpa' in data and data.get('cgpa') is not None:
            try:
                cgpa_val = float(data.get('cgpa'))
            except (TypeError, ValueError):
                return jsonify({'error': 'CGPA must be a number'}), 400
            if cgpa_val < 0 or cgpa_val > 10:
                return jsonify({'error': 'CGPA must be between 0 and 10'}), 400
            student.cgpa = cgpa_val

        if 'year' in data and data.get('year') is not None:
            try:
                student.year = int(data.get('year'))
            except (TypeError, ValueError):
                return jsonify({'error': 'Year must be a number'}), 400

        if 'first_name' in data and data.get('first_name'):
            student.first_name = data.get('first_name')
        if 'last_name' in data:
            student.last_name = data.get('last_name')
        if 'phone' in data:
            student.phone = data.get('phone')
        if 'branch' in data:
            student.branch = data.get('branch')
        if 'bio' in data:
            student.bio = data.get('bio')

        db.session.commit()
        clear_student_cache(student.id)

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'roll_number': student.roll_number,
                'phone': student.phone,
                'branch': student.branch,
                'year': student.year,
                'cgpa': student.cgpa,
                'bio': student.bio
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
