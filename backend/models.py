from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# ============================================
# ENUMERATIONS (Fixed choices for fields)
# ============================================

class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    COMPANY = "company"
    STUDENT = "student"

class CompanyStatus(str, Enum):
    """Company approval status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class DriveStatus(str, Enum):
    """Placement drive status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class ApplicationStatus(str, Enum):
    """Application status"""
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    SELECTED = "selected"
    REJECTED = "rejected"


# ============================================
# TABLE 1: USER (Login credentials for all users)
# ============================================

class User(db.Model):
    """User model for Admin, Company, and Student"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = db.relationship('Company', back_populates='user', uselist=False, cascade='all, delete-orphan')
    student = db.relationship('Student', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


# ============================================
# TABLE 2: COMPANY (Company profile details)
# ============================================

class Company(db.Model):
    """Company model for recruitment drives"""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    hr_contact = db.Column(db.String(120), nullable=True)
    hr_email = db.Column(db.String(120), nullable=True)
    hr_phone = db.Column(db.String(15), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    approval_status = db.Column(db.String(20), default=CompanyStatus.PENDING.value)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='company')
    job_positions = db.relationship('JobPosition', back_populates='company', cascade='all, delete-orphan')
    placements = db.relationship('Placement', back_populates='company', cascade='all, delete-orphan') 
    def __repr__(self):
        return f'<Company {self.company_name}>'


# ============================================
# TABLE 3: STUDENT (Student profile details)
# ============================================

class Student(db.Model):
    """Student model for placement registration"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    branch = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    resume_url = db.Column(db.String(500), nullable=True)
    profile_pic = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='student')
    applications = db.relationship('Application', back_populates='student', cascade='all, delete-orphan')
    placements = db.relationship('Placement', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'


# ============================================
# TABLE 4: JOB_POSITION (Job postings/Placement drives)
# ============================================

class JobPosition(db.Model):
    """Job Position / Placement Drive model"""
    __tablename__ = 'job_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(500), nullable=True)
    salary_min = db.Column(db.Float, nullable=True)
    salary_max = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='INR')
    location = db.Column(db.String(200), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)
    
    min_cgpa = db.Column(db.Float, nullable=True)
    eligible_branches = db.Column(db.String(500), nullable=True)
    eligible_years = db.Column(db.String(100), nullable=True)
    max_backlog = db.Column(db.Integer, nullable=True)
    
    application_deadline = db.Column(db.DateTime, nullable=False)
    drive_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default=DriveStatus.PENDING.value)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    approved_on = db.Column(db.DateTime, nullable=True)
    
    company = db.relationship('Company', back_populates='job_positions')
    applications = db.relationship('Application', back_populates='job_position', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<JobPosition {self.job_title} - {self.company.company_name}>'


# ============================================
# TABLE 5: APPLICATION (Student applications)
# ============================================

class Application(db.Model):
    """Job Application model"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_position_id = db.Column(db.Integer, db.ForeignKey('job_positions.id'), nullable=False)
    status = db.Column(db.String(20), default=ApplicationStatus.APPLIED.value)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    shortlisted_on = db.Column(db.DateTime, nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    interview_result = db.Column(db.String(50), nullable=True)
    company_feedback = db.Column(db.Text, nullable=True)
    interview_link = db.Column(db.String(500), nullable=True)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'job_position_id', name='unique_student_job_application'),)
    
    student = db.relationship('Student', back_populates='applications')
    job_position = db.relationship('JobPosition', back_populates='applications')
    
    def __repr__(self):
        return f'<Application {self.student.first_name} -> {self.job_position.job_title}>'


# ============================================
# TABLE 6: PLACEMENT (Final placements)
# ============================================

class Placement(db.Model):
    """Placement record after student is selected"""
    __tablename__ = 'placements'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_position_id = db.Column(db.Integer, db.ForeignKey('job_positions.id'), nullable=True)
    job_title = db.Column(db.String(150), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    joining_date = db.Column(db.Date, nullable=True)
    bond_period = db.Column(db.Integer, nullable=True)
    offer_letter_url = db.Column(db.String(500), nullable=True)
    placed_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Active')
    
    student = db.relationship('Student', back_populates='placements')
    company = db.relationship('Company', back_populates='placements')
    
    def __repr__(self):
        return f'<Placement {self.student.first_name} - {self.job_title}>'


# ============================================
# TABLE 7: ADMIN (Admin details)
# ============================================

class Admin(db.Model):
    """Admin user (Institute Placement Cell)"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(120), nullable=True)
    contact = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Admin {self.name}>'


# ============================================
# Cache invalidation via SQLAlchemy events
# When Company / Student / JobPosition data changes, drop the related cache
# so the next read rebuilds a fresh copy. Wrapped in try/except so a Redis
# outage never breaks a database write.
# ============================================
from sqlalchemy import event as _sa_event
from cache import cache_delete as _cache_delete


def _safe_delete(key):
    try:
        _cache_delete(key)
    except Exception:
        pass


def _invalidate_companies(mapper, connection, target):
    _safe_delete('admin_all_companies')


def _invalidate_students(mapper, connection, target):
    _safe_delete('admin_all_students')


def _invalidate_jobs(mapper, connection, target):
    _safe_delete('available_jobs_raw')


for _evt in ('after_insert', 'after_update', 'after_delete'):
    _sa_event.listen(Company, _evt, _invalidate_companies)
    _sa_event.listen(Student, _evt, _invalidate_students)
    _sa_event.listen(JobPosition, _evt, _invalidate_jobs)
