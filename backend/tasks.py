from celery_config import celery_app
from models import JobPosition, db, Student, Application, Placement, Company, User
from datetime import datetime, timedelta
from sqlalchemy import func
import csv
from io import StringIO
# ============================================
# 1. DAILY REMINDER - Send emails to students
# ============================================

@celery_app.task(name='send_daily_reminders')
def send_daily_reminders():
    """
    Scheduled task: Runs daily
    Sends reminders to students about upcoming application deadlines
    """
    try:
        from models import JobPosition
        
        # Get jobs with deadlines in next 7 days
        today = datetime.utcnow()
        week_later = today + timedelta(days=7)
        
        jobs = JobPosition.query.filter(
            JobPosition.application_deadline.between(today, week_later),
            JobPosition.status == 'approved'
        ).all()
        
        reminder_count = 0
        
        for job in jobs:
            # Get students who haven't applied yet
            students = Student.query.all()
            
            for student in students:
                # Check if student already applied
                existing_app = Application.query.filter_by(
                    student_id=student.id,
                    job_position_id=job.id
                ).first()
                
                if not existing_app:
                    # Check eligibility
                    is_eligible = True
                    
                    if job.min_cgpa and student.cgpa < job.min_cgpa:
                        is_eligible = False
                    
                    if job.eligible_branches:
                        branches = [b.strip() for b in job.eligible_branches.split(',')]
                        if student.branch not in branches:
                            is_eligible = False
                    
                    if is_eligible:
                        # In real app, send email here
                        # For now, just count
                        reminder_count += 1
        
        return {
            'success': True,
            'message': f'Daily reminders sent to {reminder_count} students',
            'reminders_sent': reminder_count
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ============================================
# 2. MONTHLY REPORT - Generate placement report
# ============================================

@celery_app.task(name='generate_monthly_report')
def generate_monthly_report():
    """
    Scheduled task: Runs on 1st of every month
    Generates placement activity report for admin
    """
    try:
        # Get current month data
        today = datetime.utcnow()
        month_start = today.replace(day=1)
        
        # Count this month's activities
        applications_this_month = Application.query.filter(
            Application.applied_on >= month_start
        ).count()
        
        placements_this_month = Placement.query.filter(
            Placement.placed_on >= month_start
        ).count()
        
        companies_registered = Company.query.filter(
            Company.created_at >= month_start
        ).count()
        
        # Calculate average salary
        placements = Placement.query.filter(
            Placement.placed_on >= month_start
        ).all()
        
        total_salary = sum([p.salary for p in placements if p.salary])
        avg_salary = total_salary / len(placements) if placements else 0
        
        # Generate report
        report = {
            'month': today.strftime('%B %Y'),
            'statistics': {
                'applications_received': applications_this_month,
                'students_selected': placements_this_month,
                'companies_registered': companies_registered,
                'average_salary': avg_salary,
                'total_salary_offered': total_salary
            },
            'generated_on': datetime.utcnow().isoformat()
        }
        
        return {
            'success': True,
            'message': 'Monthly report generated',
            'report': report
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ============================================
# 3. USER-TRIGGERED: Export applications as CSV
# ============================================

@celery_app.task(name='export_student_applications')
def export_student_applications(student_id):
    """
    User-triggered task: Student exports their applications
    Generates CSV file with application history
    """
    try:
        # Query student directly
        student = Student.query.get(student_id)
        
        if not student:
            return {
                'success': False,
                'error': 'Student not found'
            }
        
        # Get all applications
        applications = Application.query.filter_by(student_id=student_id).all()
        
        if not applications:
            return {
                'success': True,
                'message': 'CSV exported successfully (no applications)',
                'filename': f'applications_{student.roll_number}.csv',
                'data': 'Student Name,Roll Number,Company Name,Job Title,Application Status,Applied On,Shortlisted On,Interview Date,Result\n'
            }
        
        # Create CSV
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        
        # Write header
        writer.writerow([
            'Student Name',
            'Roll Number',
            'Company Name',
            'Job Title',
            'Application Status',
            'Applied On',
            'Shortlisted On',
            'Interview Date',
            'Result'
        ])
        
        # Write data
        for app_record in applications:
            job = JobPosition.query.get(app_record.job_position_id)
            company = Company.query.get(job.company_id)
            
            writer.writerow([
                f'{student.first_name} {student.last_name}',
                student.roll_number,
                company.company_name if company else 'N/A',
                job.job_title,
                app_record.status,
                app_record.applied_on.strftime('%Y-%m-%d %H:%M:%S'),
                app_record.shortlisted_on.strftime('%Y-%m-%d %H:%M:%S') if app_record.shortlisted_on else 'N/A',
                app_record.interview_date.strftime('%Y-%m-%d %H:%M:%S') if app_record.interview_date else 'N/A',
                app_record.interview_result or 'Pending'
            ])
        
        # Get CSV content
        csv_content = csv_buffer.getvalue()
        
        return {
            'success': True,
            'message': 'CSV exported successfully',
            'filename': f'applications_{student.roll_number}.csv',
            'data': csv_content
        }
    
    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }