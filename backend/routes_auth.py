from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, UserRole, Company, Student, Admin
from datetime import datetime, timedelta
from decorators import login_required, role_required, any_role_required
# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ============================================
# 1. LOGIN ENDPOINT
# ============================================

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'User account is deactivated'}), 403
        
        # Verify password
        if not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check blacklist status for students and companies
        if user.role == UserRole.STUDENT.value:
            student = Student.query.filter_by(user_id=user.id).first()
            if student and student.is_blacklisted:
                return jsonify({'error': 'Your account has been blacklisted. Contact admin.'}), 403

        if user.role == UserRole.COMPANY.value:
            company = Company.query.filter_by(user_id=user.id).first()
            if company and company.is_blacklisted:
                return jsonify({'error': 'Your company has been blacklisted. Contact admin.'}), 403
        

        # Create JWT token (expires in 7 days)
        expires = timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id),  # Convert to string!
            additional_claims={'role': user.role, 'email': user.email},
            expires_delta=expires
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


# ============================================
# 2. REGISTER ENDPOINT (For Student)
# ============================================

@auth_bp.route('/register-student', methods=['POST'])
def register_student():
    """
    Student registration endpoint
    Expected JSON:
    {
        "email": "student@college.com",
        "password": "password123",
        "first_name": "Rahul",
        "last_name": "Kumar",
        "roll_number": "CSE-001",
        "branch": "CSE",
        "year": 4,
        "cgpa": 8.5
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name', '')
        roll_number = data.get('roll_number')
        branch = data.get('branch')
        year = data.get('year')
        cgpa = data.get('cgpa')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Create user
        user = User(
            username=email.split('@')[0],
            email=email,
            password_hash=password_hash,
            role=UserRole.STUDENT.value,
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        # Create student profile
        student = Student(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            roll_number=roll_number,
            branch=branch,
            year=year,
            cgpa=cgpa
        )
        db.session.add(student)
        db.session.commit()
        
        # Create JWT token automatically after registration
        expires = timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role, 'email': user.email},
            expires_delta=expires
        )
        
        return jsonify({
            'success': True,
            'message': 'Student registered successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 3. REGISTER ENDPOINT (For Company)
# ============================================

@auth_bp.route('/register-company', methods=['POST'])
def register_company():
    """
    Company registration endpoint
    Expected JSON:
    {
        "email": "hr@tcs.com",
        "password": "password123",
        "company_name": "Tata Consultancy Services",
        "industry": "IT",
        "website": "https://www.tcs.com",
        "hr_email": "recruitment@tcs.com",
        "hr_phone": "9876543210",
        "location": "Bangalore"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['email', 'password', 'company_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('company_name')
        industry = data.get('industry')
        website = data.get('website')
        hr_email = data.get('hr_email')
        hr_phone = data.get('hr_phone')
        location = data.get('location')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Create user
        # Build a unique username; fall back to email-based if taken
        base_username = company_name.lower().replace(' ', '_')
        username = base_username
        if User.query.filter_by(username=username).first():
            username = email.split('@')[0].lower().replace('.', '_')
            if User.query.filter_by(username=username).first():
                username = f"{base_username}_{email.split('@')[0]}"
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=UserRole.COMPANY.value,
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        # Create company profile (status is PENDING by default)
        company = Company(
            user_id=user.id,
            company_name=company_name,
            industry=industry,
            website=website,
            hr_email=hr_email,
            hr_phone=hr_phone,
            location=location,
            approval_status='pending'
        )
        db.session.add(company)
        db.session.commit()
        
        # Create JWT token automatically after registration
        expires = timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role, 'email': user.email},
            expires_delta=expires
        )
        
        return jsonify({
            'success': True,
            'message': 'Company registered successfully. Waiting for admin approval.',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'approval_status': 'pending'
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# ============================================
# 4. GET CURRENT USER ENDPOINT
# ============================================

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@login_required
def get_current_user():
    """
    Get current logged-in user info
    Requires: JWT token in header
    """
    try:
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
