from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User, Student, JobPosition, Application, Placement, Company
from decorators import role_required
from datetime import datetime
from cache import cache_get, cache_set
import json
from werkzeug.utils import secure_filename
import os
# Create a Blueprint for student routes
student_bp = Blueprint('student', __name__, url_prefix='/api/student')


def clear_student_cache(student_id):
    # Invalidate the shared student jobs cache after a new application.
    cache_set('available_jobs', None, timeout=1)

# ============================================
# 1. STUDENT DASHBOARD
# ============================================

@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('student')
def student_dashboard():
    """
    Student dashboard showing statistics
    """
    try:
        # Get current user ID from JWT token
        user_id = get_jwt_identity()
        
        # Find the student for this user
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Count student's applications
        total_applications = Application.query.filter_by(student_id=student.id).count()
        
        # Count shortlisted applications
        shortlisted = Application.query.filter_by(
            student_id=student.id,
            status='shortlisted'
        ).count()
        
        # Count selected/placed
        selected = Application.query.filter_by(
            student_id=student.id,
            status='selected'
        ).count()
        
        # Count placements
        total_placements = Placement.query.filter_by(student_id=student.id).count()
        applications = Application.query.filter_by(
                student_id=student.id
            ).all()

        for app in applications:
                print(
                    app.id,
                    app.status
                )
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
    
# ============================================
# 2. VIEW AVAILABLE JOB POSITIONS
# ============================================

@student_bp.route('/jobs', methods=['GET'])
@jwt_required()
@role_required('student')
def get_available_jobs():
    """
    Get list of approved job positions that student can apply to
    CACHING: 5 minutes
    """
    try:
        # Step 1: Check if data is in cache
        cached_jobs = cache_get('available_jobs')
        if cached_jobs:
            return jsonify(cached_jobs), 200
        
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get search query (optional)
        search_query = request.args.get('search', '').lower()
        
        # Get only APPROVED job positions
        jobs = JobPosition.query.filter_by(status='approved').all()
        
        # Filter by search if provided
        if search_query:
            jobs = [j for j in jobs if 
                   search_query in j.job_title.lower() or
                   search_query in j.job_description.lower()]
        
        job_list = []
        for job in jobs:
            # Check if student is eligible
            is_eligible = True
            reasons = []
            
            # Check CGPA
            if job.min_cgpa and student.cgpa < job.min_cgpa:
                is_eligible = False
                reasons.append(f'CGPA {student.cgpa} < required {job.min_cgpa}')
            
            # Check branch
            if job.eligible_branches:
                branches = [b.strip() for b in job.eligible_branches.split(',')]
                if student.branch not in branches:
                    is_eligible = False
                    reasons.append(f'Branch {student.branch} not eligible')
            
            # Check year
            if job.eligible_years:
                years = [int(y.strip()) for y in job.eligible_years.split(',')]
                if student.year not in years:
                    is_eligible = False
                    reasons.append(f'Year {student.year} not eligible')
            
            from models import Company
            company = Company.query.get(job.company_id)
            
            job_list.append({
                'id': job.id,
                'job_title': job.job_title,
                'company_name': company.company_name if company else None,
                'company_id': job.company_id,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'location': job.location,
                'min_cgpa': job.min_cgpa,
                'eligible_branches': job.eligible_branches,
                'eligible_years': job.eligible_years,
                'application_deadline': job.application_deadline.isoformat(),
                'is_eligible': is_eligible,
                'ineligibility_reasons': reasons if not is_eligible else []
            })
        
        response_data = {
            'success': True,
            'total': len(job_list),
            'jobs': job_list
        }
        
        # Step 2: Store in cache for 5 minutes
        cache_set('available_jobs', response_data, timeout=300)
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ============================================
# 3. APPLY FOR JOB POSITION
# ============================================

@student_bp.route('/apply-job/<int:job_id>', methods=['POST'])
@jwt_required()
@role_required('student')
def apply_for_job(job_id):
    """
    Student applies for a job position
    Checks eligibility and prevents duplicate applications
    """
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Find the job
        job = JobPosition.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check if job is approved
        if job.status != 'approved':
            return jsonify({'error': 'This job is not available for applications'}), 400
        
        # Check if student already applied
        existing_application = Application.query.filter_by(
            student_id=student.id,
            job_position_id=job_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'You have already applied for this job'}), 400
        
        # Check eligibility
        if job.min_cgpa and student.cgpa < job.min_cgpa:
            return jsonify({'error': f'Your CGPA {student.cgpa} is below required {job.min_cgpa}'}), 400
        
        if job.eligible_branches:
            branches = [b.strip() for b in job.eligible_branches.split(',')]
            if student.branch not in branches:
                return jsonify({'error': f'Your branch {student.branch} is not eligible'}), 400
        
        if job.eligible_years:
            years = [int(y.strip()) for y in job.eligible_years.split(',')]
            if student.year not in years:
                return jsonify({'error': f'Your year {student.year} is not eligible'}), 400
        
        # Create application
        application = Application(
            student_id=student.id,
            job_position_id=job_id,
            status='applied',
            applied_on=datetime.utcnow()
        )
        
        db.session.add(application)
        db.session.commit()

        # Clear job cache when student applies
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
    
# ============================================
# 4. VIEW STUDENT'S APPLICATIONS
# ============================================

@student_bp.route('/my-applications', methods=['GET'])
@jwt_required()
@role_required('student')
def get_student_applications():
    """
    Get all applications submitted by this student
    """
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get all applications for this student
        applications = Application.query.filter_by(student_id=student.id).all()
        
        app_list = []
        for app in applications:
            job = JobPosition.query.get(app.job_position_id)
            from models import Company
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
        
        return jsonify({
            'success': True,
            'total': len(app_list),
            'applications': app_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 5. VIEW STUDENT'S PLACEMENTS
# ============================================

@student_bp.route('/placements', methods=['GET'])
@jwt_required()
@role_required('student')
def get_student_placements():
    """
    Student views their placement records
    Shows all companies they got placed at
    """
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get all placements for this student
        placements = Placement.query.filter_by(student_id=student.id).all()
        
        placement_list = []
        for placement in placements:
            company = Company.query.get(placement.company_id)
            
            placement_list.append({
                'placement_id': placement.id,
                'company_name': company.company_name if company else None,
                'job_title': placement.job_title,
                'salary': placement.salary,
                'currency': placement.currency,
                'joining_date': placement.joining_date.isoformat() if placement.joining_date else None,
                'bond_period': placement.bond_period,
                'status': placement.status,
                'placed_on': placement.placed_on.isoformat()
            })
        
        return jsonify({
            'success': True,
            'total': len(placement_list),
            'placements': placement_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 6. EXPORT APPLICATIONS AS CSV
# ============================================

@student_bp.route('/export-applications', methods=['POST'])
@jwt_required()
@role_required('student')
def export_applications():
    """
    Student triggers CSV export of their applications
    Runs as background task
    """
    try:
        from celery_config import celery_app
        from tasks import export_student_applications
        
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=int(user_id)).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Trigger background task
        task = export_student_applications.delay(student.id)
        
        return jsonify({
            'success': True,
            'message': 'Export started. You will receive your CSV shortly.',
            'task_id': task.id
        }), 202  # 202 = Accepted (processing)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# 7. CHECK EXPORT STATUS
# ============================================

@student_bp.route('/export-status/<task_id>', methods=['GET'])
@jwt_required()
@role_required('student')
def check_export_status(task_id):
    """
    Check status of export task
    """
    try:
        from celery_config import celery_app
        
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            return jsonify({
                'success': True,
                'status': 'pending',
                'message': 'Export is being processed...'
            }), 200
        
        elif task_result.state == 'SUCCESS':
            return jsonify({
                'success': True,
                'status': 'completed',
                'message': 'Export completed!',
                'data': task_result.result
            }), 200
        
        elif task_result.state == 'FAILURE':
            return jsonify({
                'success': False,
                'status': 'failed',
                'error': str(task_result.info)
            }), 400
        
        else:
            return jsonify({
                'success': True,
                'status': task_result.state.lower(),
                'message': f'Export status: {task_result.state}'
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#  Resume_Upload

@student_bp.route('/upload-resume', methods=['POST'])
@jwt_required()
@role_required('student')
def upload_resume():
    try:
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']

        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400

        filename = secure_filename(
            f"{student.id}_{file.filename}"
        )

        upload_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            filename
        )

        file.save(upload_path)

        student.resume_url = (
            f"/uploads/resumes/{filename}"
        )

        db.session.commit()

        return jsonify({
            'success': True,
            'resume_url': student.resume_url,
            'message': 'Resume uploaded successfully'
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500