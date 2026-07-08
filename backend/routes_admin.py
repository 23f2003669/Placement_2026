from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User, Company, Student, JobPosition, Application, Placement
from decorators import role_required
from sqlalchemy import func
from datetime import datetime
from cache import cache_get, cache_set, cache_delete

# Create a Blueprint for admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ============================================
# 1. ADMIN DASHBOARD - Get Statistics
# ============================================

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    """
    Admin dashboard showing key statistics
    CACHING: 30 minutes
    """
    try:
        # # Check cache first
        # cached_data = cache_get('admin_dashboard')
        # if cached_data:
        #     return jsonify(cached_data), 200
        
        # Count total students
        total_students = Student.query.count()
        
        # Count total companies
        total_companies = Company.query.count()
        
        # Count approved companies
        approved_companies = Company.query.filter_by(approval_status='approved').count()
        
        # Count pending companies
        pending_companies = Company.query.filter_by(approval_status='pending').count()
        
        # Count total job positions
        total_job_positions = JobPosition.query.count()
        
        # Count approved job positions
        approved_jobs = JobPosition.query.filter_by(status='approved').count()
        
        # Count pending job positions
        pending_jobs = JobPosition.query.filter_by(status='pending').count()
        
        # Count total applications
        total_applications = Application.query.count()
        
        # Count total placements
        total_placements = Placement.query.count()
        
        response_data = {
            'success': True,
            'data': {
                'students': {'total': total_students},
                'companies': {
                    'total': total_companies,
                    'approved': approved_companies,
                    'pending': pending_companies
                },
                'job_positions': {
                    'total': total_job_positions,
                    'approved': approved_jobs,
                    'pending': pending_jobs
                },
                'applications': {'total': total_applications},
                'placements': {'total': total_placements}
            }
        }
        
        # Cache for 30 minutes
        # cache_set('admin_dashboard', response_data, timeout=1800)
        
        return jsonify(response_data), 200
    
    except Exception as e:
            print("\n===== DASHBOARD ERROR =====")
            print(repr(e))

            import traceback
            traceback.print_exc()

            return jsonify({
                'error': str(e)
            }), 500
    
# ============================================
# 2. VIEW ALL COMPANIES
# ============================================

@admin_bp.route('/companies', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_companies():
    """
    List all companies (admin). Raw list cached for 5 minutes; the search
    filter is applied on the cached list each request.
    """
    try:
        search_query = request.args.get('search', '').lower()

        company_list = cache_get('admin_all_companies')
        if company_list is None:
            companies = Company.query.all()
            company_list = []
            for company in companies:
                company_list.append({
                    'id': company.id,
                    'company_name': company.company_name,
                    'industry': company.industry,
                    'website': company.website,
                    'hr_email': company.hr_email,
                    'hr_phone': company.hr_phone,
                    'location': company.location,
                    'approval_status': company.approval_status,
                    'is_blacklisted': company.is_blacklisted,
                    'created_at': company.created_at.isoformat()
                })
            cache_set('admin_all_companies', company_list, timeout=300)

        if search_query:
            company_list = [c for c in company_list if
                            search_query in c['company_name'].lower() or
                            search_query in (c['industry'] or '').lower()]

        return jsonify({
            'success': True,
            'total': len(company_list),
            'companies': company_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# ============================================
# 3. APPROVE COMPANY REGISTRATION
# ============================================

@admin_bp.route('/approve-company/<int:company_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def approve_company(company_id):
    """
    Admin approves a company registration
    Once approved, company can create job postings
    """
    try:
        # Find company
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Check if already approved
        if company.approval_status == 'approved':
            return jsonify({'error': 'Company already approved'}), 400
        
        # Update status
        company.approval_status = 'approved'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{company.company_name} approved successfully',
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'approval_status': company.approval_status
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 4. REJECT COMPANY REGISTRATION
# ============================================

@admin_bp.route('/reject-company/<int:company_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def reject_company(company_id):
    """
    Admin rejects a company registration
    Company cannot post jobs and must reapply
    """
    try:
        # Find company
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Check if already rejected
        if company.approval_status == 'rejected':
            return jsonify({'error': 'Company already rejected'}), 400
        
        # Update status
        company.approval_status = 'rejected'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{company.company_name} rejected',
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'approval_status': company.approval_status
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 5. VIEW ALL STUDENTS
# ============================================

@admin_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_students():
    """
    List all students (admin). Raw list cached for 5 minutes; the search
    filter is applied on the cached list each request.
    """
    try:
        search_query = request.args.get('search', '').lower()

        student_list = cache_get('admin_all_students')
        if student_list is None:
            students = Student.query.all()
            student_list = []
            for student in students:
                user = User.query.get(student.user_id)
                student_list.append({
                    'id': student.id,
                    'user_id': student.user_id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': user.email if user else None,
                    'roll_number': student.roll_number,
                    'branch': student.branch,
                    'year': student.year,
                    'cgpa': student.cgpa,
                    'is_blacklisted': student.is_blacklisted,
                    'created_at': student.created_at.isoformat()
                })
            cache_set('admin_all_students', student_list, timeout=300)

        if search_query:
            student_list = [s for s in student_list if
                            search_query in s['first_name'].lower() or
                            search_query in (s['last_name'] or '').lower() or
                            search_query in (s['roll_number'] or '').lower()]

        return jsonify({
            'success': True,
            'total': len(student_list),
            'students': student_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# 6. BLACKLIST STUDENT
# ============================================

@admin_bp.route('/blacklist-student/<int:student_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def blacklist_student(student_id):
    """
    Admin blacklists a student
    Blacklisted student cannot login
    """
    try:
        # Find student
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check if already blacklisted
        if student.is_blacklisted:
            return jsonify({'error': 'Student already blacklisted'}), 400
        
        # Blacklist the student
        student.is_blacklisted = True
        
        # Also deactivate the user account
        user = User.query.get(student.user_id)
        if user:
            user.is_active = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{student.first_name} {student.last_name} has been blacklisted',
            'student': {
                'id': student.id,
                'name': f'{student.first_name} {student.last_name}',
                'is_blacklisted': student.is_blacklisted
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

# ============================================
# 7. BLACKLIST COMPANY
# ============================================

@admin_bp.route('/blacklist-company/<int:company_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def blacklist_company(company_id):
    """
    Admin blacklists a company
    Blacklisted company cannot post jobs
    """
    try:
        # Find company
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Check if already blacklisted
        if company.is_blacklisted:
            return jsonify({'error': 'Company already blacklisted'}), 400
        
        # Blacklist the company
        company.is_blacklisted = True
        
        # Also deactivate the user account
        user = User.query.get(company.user_id)
        if user:
            user.is_active = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{company.company_name} has been blacklisted',
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'is_blacklisted': company.is_blacklisted
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 8. VIEW ALL JOB POSITIONS
# ============================================

@admin_bp.route('/job-positions', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_job_positions():
    """
    Get list of all job positions with their approval status
    Only admin can access this
    """
    try:
        # Get all job positions
        jobs = JobPosition.query.all()
        
        job_list = []
        for job in jobs:
            company = Company.query.get(job.company_id)
            job_list.append({
                'id': job.id,
                'job_title': job.job_title,
                'company_name': company.company_name if company else None,
                'company_id': job.company_id,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'min_cgpa': job.min_cgpa,
                'eligible_branches': job.eligible_branches,
                'status': job.status,
                'application_deadline': job.application_deadline.isoformat(),
                'posted_on': job.posted_on.isoformat()
            })
        
        return jsonify({
            'success': True,
            'total': len(job_list),
            'job_positions': job_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 9. APPROVE JOB POSITION
# ============================================

@admin_bp.route('/approve-job/<int:job_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def approve_job_position(job_id):
    """
    Admin approves a job posting
    Once approved, students can see and apply for this job
    """
    try:
        # Find job position
        job = JobPosition.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job position not found'}), 404
        
        # Check if already approved
        if job.status == 'approved':
            return jsonify({'error': 'Job already approved'}), 400
        
        # Update status
        job.status = 'approved'
        job.approved_on = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{job.job_title} approved successfully',
            'job': {
                'id': job.id,
                'job_title': job.job_title,
                'status': job.status
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================
# 9. REJECT JOB POSITION
# ============================================

@admin_bp.route('/reject-job/<int:job_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def reject_job_position(job_id):
    try:
        job = JobPosition.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job position not found'}), 404
        if job.status == 'rejected':
            return jsonify({'error': 'Job already rejected'}), 400
        job.status = 'rejected'
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'{job.job_title} rejected',
            'job': {
                'id': job.id,
                'job_title': job.job_title,
                'status': job.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500        
    
# ============================================
# 10. UNBLACKLIST STUDENT
# ============================================

@admin_bp.route('/unblacklist-student/<int:student_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def unblacklist_student(student_id):
    """
    Admin removes a student from blacklist
    Student can login again
    """
    try:
        # Find student
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check if student is actually blacklisted
        if not student.is_blacklisted:
            return jsonify({'error': 'Student is not blacklisted'}), 400
        
        # Remove from blacklist
        student.is_blacklisted = False
        
        # Reactivate the user account
        user = User.query.get(student.user_id)
        if user:
            user.is_active = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{student.first_name} {student.last_name} has been removed from blacklist',
            'student': {
                'id': student.id,
                'name': f'{student.first_name} {student.last_name}',
                'is_blacklisted': student.is_blacklisted
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 11. UNBLACKLIST COMPANY
# ============================================

@admin_bp.route('/unblacklist-company/<int:company_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def unblacklist_company(company_id):
    """
    Admin removes a company from blacklist
    Company can post jobs again
    """
    try:
        # Find company
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Check if company is actually blacklisted
        if not company.is_blacklisted:
            return jsonify({'error': 'Company is not blacklisted'}), 400
        
        # Remove from blacklist
        company.is_blacklisted = False
        
        # Reactivate the user account
        user = User.query.get(company.user_id)
        if user:
            user.is_active = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{company.company_name} has been removed from blacklist',
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'is_blacklisted': company.is_blacklisted
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 12. VIEW ALL APPLICATIONS
# ============================================

@admin_bp.route('/applications', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_applications():
    """
    Admin views all applications in the system
    Can search/filter by student name, company, job, status
    """
    try:
        # Get filter parameters
        status_filter = request.args.get('status')
        search_query = request.args.get('search', '').lower()
        
        # Get all applications
        applications = Application.query.all()
        
        # Filter by status if provided
        if status_filter:
            applications = [a for a in applications if a.status == status_filter]
        
        # Filter by search query
        if search_query:
            applications = [a for a in applications if 
                          search_query in Student.query.get(a.student_id).first_name.lower() or
                          search_query in Student.query.get(a.student_id).last_name.lower() or
                          search_query in JobPosition.query.get(a.job_position_id).job_title.lower()]
        
        app_list = []
        for app in applications:
            student = Student.query.get(app.student_id)
            job = JobPosition.query.get(app.job_position_id)
            company = Company.query.get(job.company_id)
            user = User.query.get(student.user_id)
            
            app_list.append({
                'application_id': app.id,
                'student_name': f'{student.first_name} {student.last_name}',
                'student_email': user.email,
                'company_name': company.company_name if company else None,
                'job_title': job.job_title,
                'status': app.status,
                'applied_on': app.applied_on.isoformat(),
                'shortlisted_on': app.shortlisted_on.isoformat() if app.shortlisted_on else None,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None
            })
        
        return jsonify({
            'success': True,
            'total': len(app_list),
            'applications': app_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 13. VIEW ALL PLACEMENTS
# ============================================

@admin_bp.route('/placements', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_placements():
    """
    Admin views all placements in the system
    For generating placement statistics and reports
    """
    try:
        # Get all placements
        placements = Placement.query.all()
        
        placement_list = []
        for placement in placements:
            student = Student.query.get(placement.student_id)
            company = Company.query.get(placement.company_id)
            user = User.query.get(student.user_id)
            
            placement_list.append({
                'placement_id': placement.id,
                'student_name': f'{student.first_name} {student.last_name}',
                'student_email': user.email,
                'student_branch': student.branch,
                'student_cgpa': student.cgpa,
                'company_name': company.company_name if company else None,
                'job_title': placement.job_title,
                'salary': placement.salary,
                'currency': placement.currency,
                'joining_date': placement.joining_date.isoformat() if placement.joining_date else None,
                'status': placement.status,
                'placed_on': placement.placed_on.isoformat()
            })
        
        # Calculate stats
        total_placements = len(placement_list)
        total_salary = sum([p['salary'] for p in placement_list if p['salary']])
        avg_salary = total_salary / total_placements if total_placements > 0 else 0
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_placements': total_placements,
                'total_salary_offered': total_salary,
                'average_salary': avg_salary
            },
            'placements': placement_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

# ============================================
# ANALYTICS - aggregated data for dashboard charts
# ============================================

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_analytics():
    """Aggregated counts for admin dashboard charts."""
    try:
        status_rows = db.session.query(
            Application.status, func.count(Application.id)
        ).group_by(Application.status).all()
        application_status = {str(s): c for s, c in status_rows}

        branch_rows = db.session.query(
            Student.branch, func.count(Student.id)
        ).group_by(Student.branch).all()
        students_by_branch = {(b or 'Unknown'): c for b, c in branch_rows}

        job_rows = db.session.query(
            JobPosition.status, func.count(JobPosition.id)
        ).group_by(JobPosition.status).all()
        jobs_by_status = {str(s): c for s, c in job_rows}

        return jsonify({
            'success': True,
            'analytics': {
                'application_status': application_status,
                'students_by_branch': students_by_branch,
                'jobs_by_status': jobs_by_status
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
