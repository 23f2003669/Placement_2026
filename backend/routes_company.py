from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User, Company, Student, JobPosition, Application, Placement
from decorators import role_required
from datetime import datetime
from cache import cache_get, cache_set, cache_delete

# Create a Blueprint for company routes
company_bp = Blueprint('company', __name__, url_prefix='/api/company')

# ============================================
# 1. COMPANY DASHBOARD
# ============================================

@company_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('company')
def company_dashboard():
    """
    Company dashboard showing statistics
    Only approved companies can access
    """
    try:
        # Get current user ID from JWT token
        user_id = get_jwt_identity()
        
        # Find the company for this user
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Check if company is blacklisted
        if company.is_blacklisted:
            return jsonify({'error': 'Your company has been blacklisted'}), 403
             

        if company.approval_status == 'pending':
            return jsonify({'error': 'pending'}), 403

        if company.approval_status == 'rejected':
            return jsonify({'error': 'rejected'}), 403
            
        # Count company's job positions
        total_jobs = JobPosition.query.filter_by(company_id=company.id).count()
        
        # Count total applicants for all jobs
        total_applicants = 0
        company_jobs = JobPosition.query.filter_by(company_id=company.id).all()
        for job in company_jobs:
            applicants = Application.query.filter_by(job_position_id=job.id).count()
            total_applicants += applicants
        
        # Count shortlisted candidates
        shortlisted = 0
        for job in company_jobs:
            shortlisted += Application.query.filter_by(
                job_position_id=job.id,
                status='shortlisted'
            ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'company': {
                    'id': company.id,
                    'company_name': company.company_name,
                    'approval_status': company.approval_status,
                    'industry': company.industry,
                    'location': company.location,
                    'website': company.website
                },
                'statistics': {
                    'total_jobs': total_jobs,
                    'total_applicants': total_applicants,
                    'shortlisted_candidates': shortlisted
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 2. CREATE JOB POSITION
# ============================================

@company_bp.route('/create-job', methods=['POST'])
@jwt_required()
@role_required('company')
def create_job():
    """
    Company creates a new job position
    Job status is PENDING until admin approves it
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        if company.is_blacklisted:
            return jsonify({'error': 'Your company has been blacklisted'}), 403
        
        if company.approval_status != 'approved':
            return jsonify({'error': 'Only approved companies can create jobs'}), 403
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['job_title', 'job_description', 'application_deadline']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        skills_required = data.get('skills_required')
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')
        location = data.get('location', company.location)
        job_type = data.get('job_type')
        min_cgpa = data.get('min_cgpa')
        eligible_branches = data.get('eligible_branches')
        eligible_years = data.get('eligible_years')
        max_backlog = data.get('max_backlog')
        application_deadline_str = data.get('application_deadline')
        
        # Convert string to datetime if provided
        if application_deadline_str:
            try:
                # Try to parse the ISO format string
                application_deadline = datetime.fromisoformat(application_deadline_str.replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid date format. Use ISO format: 2026-06-30T23:59:59'}), 400
        else:
            return jsonify({'error': 'application_deadline is required'}), 400
        
        # Create job position
        job = JobPosition(
            company_id=company.id,
            job_title=job_title,
            job_description=job_description,
            skills_required=skills_required,
            salary_min=salary_min,
            salary_max=salary_max,
            location=location,
            job_type=job_type,
            min_cgpa=min_cgpa,
            eligible_branches=eligible_branches,
            eligible_years=eligible_years,
            max_backlog=max_backlog,
            application_deadline=application_deadline,
            status='pending'  # Needs admin approval
        )
        
        db.session.add(job)
        db.session.commit()

        # Clear cache since jobs list changed
        cache_delete(f'company_jobs_{company.id}')
        
        return jsonify({
            'success': True,
            'message': 'Job position created successfully. Waiting for admin approval.',
            'job': {
                'id': job.id,
                'job_title': job.job_title,
                'status': job.status
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 3. VIEW COMPANY'S JOB POSITIONS
# ============================================

@company_bp.route('/my-jobs', methods=['GET'])
@jwt_required()
@role_required('company')
def get_company_jobs():
    """
    Get all job positions created by this company
    Only company can see their own jobs
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404

        # Check cache first
        cache_key = f'company_jobs_{company.id}'
        cached_data = cache_get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Get all jobs for this company
        jobs = JobPosition.query.filter_by(company_id=company.id).all()
        
        job_list = []
        for job in jobs:
            # Count applicants for this job
            applicants_count = Application.query.filter_by(job_position_id=job.id).count()
            print(f"JOB {job.id} -> Applicants = {applicants_count}")
            job_list.append({
                    'id': job.id,
                    'job_title': job.job_title,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'location': job.location,
                    'job_type': job.job_type,
                    'status': job.status,
                    'applicants_count': applicants_count,
                    'application_deadline': job.application_deadline.isoformat(),
                    'posted_on': job.posted_on.isoformat()
                })
        
        response_data = {
            'success': True,
            'total': len(job_list),
            'jobs': job_list
        }
        
        # Save to cache for 60 seconds
        cache_set(cache_key, response_data, timeout=60)
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 4. VIEW APPLICANTS FOR A JOB
# ============================================
@company_bp.route('/job/<int:job_id>/applicants', methods=['GET'])
@jwt_required()
@role_required('company')
def get_job_applicants(job_id):
    """
    Company views all applicants for a specific job
    Only the company that posted this job can see
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Find the job
        job = JobPosition.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check if this job belongs to this company
        if job.company_id != company.id:
            return jsonify({'error': 'You can only view applicants for your own jobs'}), 403
        
        # Get all applications for this job
        applications = Application.query.filter_by(job_position_id=job_id).all()
        
        applicant_list = []
        for app in applications:
            student = Student.query.get(app.student_id)
            user = User.query.get(student.user_id)
            
            applicant_list.append({
                'application_id': app.id,
                'student_id': student.id,
                'student_name': f'{student.first_name} {student.last_name}',
                'email': user.email,
                'roll_number': student.roll_number,
                'branch': student.branch,
                'year': student.year,
                'cgpa': student.cgpa,
                'resume_url': student.resume_url,
                'application_status': app.status,
                'applied_on': app.applied_on.isoformat(),
                'shortlisted_on': app.shortlisted_on.isoformat() if app.shortlisted_on else None,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'company_feedback': app.company_feedback
            })
        
        return jsonify({
            'success': True,
            'job': {
                'id': job.id,
                'job_title': job.job_title
            },
            'total_applicants': len(applicant_list),
            'applicants': applicant_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 5. SHORTLIST STUDENT FOR INTERVIEW
# ============================================

@company_bp.route('/shortlist-student/<int:application_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def shortlist_student(application_id):
    """
    Company shortlists a student for interview
    Changes application status from 'applied' to 'shortlisted'
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Find the application
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application is for a job posted by this company
        job = JobPosition.query.get(application.job_position_id)
        if job.company_id != company.id:
            return jsonify({'error': 'You can only shortlist applicants for your own jobs'}), 403
        
        # Check if already shortlisted
        if application.status == 'shortlisted':
            return jsonify({'error': 'Student already shortlisted'}), 400
        
        # Update application status
        application.status = 'shortlisted'
        application.shortlisted_on = datetime.utcnow()
        
        db.session.commit()
        
        student = Student.query.get(application.student_id)
        
        return jsonify({
            'success': True,
            'message': f'{student.first_name} {student.last_name} has been shortlisted',
            'application': {
                'id': application.id,
                'student_id': application.student_id,
                'status': application.status,
                'shortlisted_on': application.shortlisted_on.isoformat()
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 6. REJECT STUDENT APPLICATION
# ============================================

@company_bp.route('/reject-application/<int:application_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def reject_application(application_id):
    """
    Company rejects a student's application
    Can optionally provide feedback
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Find the application
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application is for a job posted by this company
        job = JobPosition.query.get(application.job_position_id)
        if job.company_id != company.id:
            return jsonify({'error': 'You can only reject applicants for your own jobs'}), 403
        
        # Check if already rejected
        if application.status == 'rejected':
            return jsonify({'error': 'Application already rejected'}), 400
        
        # Get feedback if provided
        data = request.get_json(silent=True)
        feedback = data.get('feedback') if data else None
        
        # Update application status
        application.status = 'rejected'
        application.company_feedback = feedback
        
        db.session.commit()
        
        student = Student.query.get(application.student_id)
        
        return jsonify({
            'success': True,
            'message': f'{student.first_name} {student.last_name} application rejected',
            'application': {
                'id': application.id,
                'student_id': application.student_id,
                'status': application.status,
                'feedback': feedback
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 7. SCHEDULE INTERVIEW
# ============================================

@company_bp.route('/schedule-interview/<int:application_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def schedule_interview(application_id):
    """
    Company schedules an interview with shortlisted student
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Find the application
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application is for a job posted by this company
        job = JobPosition.query.get(application.job_position_id)
        if job.company_id != company.id:
            return jsonify({'error': 'You can only schedule interviews for your own jobs'}), 403
        
        # Check if student is shortlisted
        if application.status != 'shortlisted':
            return jsonify({'error': 'Student must be shortlisted before scheduling interview'}), 400
        
        # Get interview date from request
        data = request.get_json()
        if not data or not data.get('interview_date'):
            return jsonify({'error': 'interview_date is required'}), 400
        
        interview_date_str = data.get('interview_date')
        
        # Convert string to datetime
        try:
            interview_date = datetime.fromisoformat(interview_date_str.replace('Z', '+00:00'))
        except:
            return jsonify({'error': 'Invalid date format. Use ISO format: 2026-06-30T10:00:00'}), 400
        
        # Update application
        application.status = 'interview'
        application.interview_date = interview_date
        
        db.session.commit()
        
        student = Student.query.get(application.student_id)
        
        return jsonify({
            'success': True,
            'message': f'Interview scheduled with {student.first_name} {student.last_name}',
            'application': {
                'id': application.id,
                'student_id': application.student_id,
                'status': application.status,
                'interview_date': application.interview_date.isoformat()
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 8. SEND INTERVIEW RESULT
# ============================================

@company_bp.route('/send-result/<int:application_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def send_interview_result(application_id):
    """
    Company sends interview result (selected or rejected)
    If selected, creates a placement record
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Find the application
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application is for a job posted by this company
        job = JobPosition.query.get(application.job_position_id)
        if job.company_id != company.id:
            return jsonify({'error': 'You can only send results for your own jobs'}), 403
        
        # Get result data
        data = request.get_json()
        if not data or not data.get('result'):
            return jsonify({'error': 'result is required (selected or rejected)'}), 400
        
        result = data.get('result').lower()
        feedback = data.get('feedback')
        
        if result not in ['selected', 'rejected']:
            return jsonify({'error': 'result must be "selected" or "rejected"'}), 400
        
        # Update application status
        if result == 'selected':
            application.status = 'selected'
            application.interview_result = 'selected'
            
            # Create placement record
            student = Student.query.get(application.student_id)
            
            # Get placement details
            salary = data.get('salary')
            joining_date_str = data.get('joining_date')
            
            # Convert string to date if provided
            joining_date = None
            if joining_date_str:
                try:
                    from datetime import datetime as dt
                    # Parse the date string (format: 2026-09-01)
                    joining_date = dt.fromisoformat(joining_date_str).date()
                except:
                    return jsonify({'error': 'Invalid date format. Use format: 2026-09-01'}), 400
            
            # Create placement  
            placement = Placement(
                student_id=application.student_id,
                company_id=company.id,
                job_position_id=job.id,
                job_title=job.job_title,
                salary=salary if salary else 0,
                joining_date=joining_date,
                status='Active'
            )
            
            db.session.add(placement)
            
            return_message = f'{student.first_name} {student.last_name} selected successfully'
            
        else:  # rejected
            application.status = 'rejected'
            application.interview_result = 'rejected'
            return_message = f'Rejection sent to student'
        
        # Add feedback if provided
        if feedback:
            application.company_feedback = feedback
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': return_message,
            'application': {
                'id': application.id,
                'student_id': application.student_id,
                'status': application.status,
                'result': result,
                'feedback': feedback
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================
# 9. CLOSE JOB POSTING
# ============================================

@company_bp.route('/close-job/<int:job_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def close_job(job_id):
    """
    Company closes a job posting (status -> closed)
    """
    try:
        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=int(user_id)).first()
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        job = JobPosition.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        if job.company_id != company.id:
            return jsonify({'error': 'You can only close your own job postings'}), 403
        
        if job.status == 'closed':
            return jsonify({'error': 'Job is already closed'}), 400
        
        job.status = 'closed'
        db.session.commit()
        
        # Clear cache since job status changed
        cache_delete(f'company_jobs_{company.id}')
        
        return jsonify({
            'success': True,
            'message': f'Job "{job.job_title}" has been closed',
            'job': {
                'id': job.id,
                'status': job.status
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500