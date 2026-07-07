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
    Scheduled task (daily): email each student a reminder listing upcoming
    application deadlines (within 7 days) for eligible jobs they have not
    yet applied to.
    """
    try:
        from email_utils import send_email

        today = datetime.utcnow()
        week_later = today + timedelta(days=7)

        jobs = JobPosition.query.filter(
            JobPosition.application_deadline.between(today, week_later),
            JobPosition.status == 'approved'
        ).all()

        students = Student.query.all()
        emails_sent = 0

        for student in students:
            eligible_jobs = []
            for job in jobs:
                existing = Application.query.filter_by(
                    student_id=student.id, job_position_id=job.id).first()
                if existing:
                    continue
                if job.min_cgpa and (student.cgpa is None or student.cgpa < job.min_cgpa):
                    continue
                if job.eligible_branches:
                    branches = [b.strip().lower() for b in job.eligible_branches.split(',')]
                    if (student.branch or '').strip().lower() not in branches:
                        continue
                eligible_jobs.append(job)

            if not eligible_jobs:
                continue

            user = User.query.get(student.user_id)
            if not user or not user.email:
                continue

            rows = ''.join(
                f"<li><strong>{j.job_title}</strong> - deadline "
                f"{j.application_deadline.strftime('%d %b %Y')}</li>"
                for j in eligible_jobs
            )
            html = (
                f"<h2>Upcoming Application Deadlines</h2>"
                f"<p>Hi {student.first_name}, these eligible jobs are closing "
                f"soon. Apply before the deadline:</p>"
                f"<ul>{rows}</ul>"
                f"<p>- Placement Portal</p>"
            )
            if send_email(user.email, 'Placement Portal - Upcoming Deadlines', html):
                emails_sent += 1

        return {
            'success': True,
            'message': f'Reminder emails sent to {emails_sent} students',
            'emails_sent': emails_sent
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============================================
# 2. MONTHLY REPORT - Generate placement report
# ============================================

@celery_app.task(name='generate_monthly_report')
def generate_monthly_report():
    """
    Scheduled task (1st of month): build an HTML placement activity report
    for the current month and email it to the admin.
    """
    try:
        import os
        from email_utils import send_email

        today = datetime.utcnow()
        month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        applications_this_month = Application.query.filter(
            Application.applied_on >= month_start).count()
        placements_this_month = Placement.query.filter(
            Placement.placed_on >= month_start).count()
        companies_registered = Company.query.filter(
            Company.created_at >= month_start).count()
        total_approved_drives = JobPosition.query.filter_by(status='approved').count()

        placements = Placement.query.filter(
            Placement.placed_on >= month_start).all()
        total_salary = sum(p.salary for p in placements if p.salary)
        avg_salary = total_salary / len(placements) if placements else 0

        html = f"""
        <h2>Placement Activity Report - {today.strftime('%B %Y')}</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
            <tr><td><strong>Total approved drives</strong></td><td>{total_approved_drives}</td></tr>
            <tr><td><strong>Applications received (this month)</strong></td><td>{applications_this_month}</td></tr>
            <tr><td><strong>Students selected / placed (this month)</strong></td><td>{placements_this_month}</td></tr>
            <tr><td><strong>Companies registered (this month)</strong></td><td>{companies_registered}</td></tr>
            <tr><td><strong>Average salary</strong></td><td>{avg_salary:.2f}</td></tr>
            <tr><td><strong>Total salary offered</strong></td><td>{total_salary}</td></tr>
        </table>
        <p>Generated on {today.strftime('%d %b %Y %H:%M')} UTC</p>
        <p>- Placement Portal</p>
        """

        admin_email = os.environ.get('ADMIN_EMAIL')
        sent = False
        if admin_email:
            sent = send_email(admin_email,
                              f'Monthly Placement Report - {today.strftime("%B %Y")}',
                              html)

        return {
            'success': True,
            'message': 'Monthly report generated' + (' and emailed' if sent else ' (email not sent)'),
            'emailed': sent
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


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