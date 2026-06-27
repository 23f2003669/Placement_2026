from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' | 'company' | 'student'
    is_active_flag = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship("Company", backref="user", uselist=False, cascade="all, delete-orphan")

    @property
    def is_active(self):
        return self.is_active_flag


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    grad_year = db.Column(db.Integer)
    skills = db.Column(db.String(300))
    resume_path = db.Column(db.String(255))
    phone = db.Column(db.String(20))

    applications = db.relationship("Application", backref="student", cascade="all, delete-orphan")


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(120))
    approval_status = db.Column(db.String(20), default="pending")  # pending | approved | rejected

    drives = db.relationship("Drive", backref="company", cascade="all, delete-orphan")


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    eligible_branches = db.Column(db.String(200))
    min_cgpa = db.Column(db.Float, default=0)
    eligible_year = db.Column(db.Integer)
    salary = db.Column(db.Float)
    location = db.Column(db.String(120))
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending | approved | rejected | closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)

    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="applied")  # applied | shortlisted | selected | rejected
    feedback = db.Column(db.String(300))

    placement = db.relationship("Placement", backref="application", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )


class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, unique=True)

    final_salary = db.Column(db.Float)
    joining_date = db.Column(db.DateTime)
    offer_letter_path = db.Column(db.String(255))