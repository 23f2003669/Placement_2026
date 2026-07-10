from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS
from config import get_config
from models import db, Student, Company, JobPosition, Application
from database import init_db
from datetime import timedelta
from celery_config import celery_app
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
def create_app(config_name='development'):
    """
    Application factory - creates and configures the Flask app
    """
    print("Starting Flask application...")
    
    # Create Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Load configuration
    print(f"Loading {config_name} configuration...")
    app.config.from_object(get_config(config_name))
    
    # Initialize database
    print("Initializing database...")
    db.init_app(app)

    # Celery app-context wrapping is handled in celery_config.init_celery()
    
    # Create database tables and admin user
    init_db(app)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    
    os.makedirs(
            app.config['UPLOAD_FOLDER'],
            exist_ok=True
      )


    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)
    
    # Import and register blueprints
    from routes_auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes_admin import admin_bp
    app.register_blueprint(admin_bp)

    from routes_company import company_bp
    app.register_blueprint(company_bp)

    from routes_student import student_bp
    app.register_blueprint(student_bp)

    from routes_public import public_bp
    app.register_blueprint(public_bp)
    
    # ============================================
    # ROUTES (API endpoints)
    # ============================================
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Simple health check endpoint"""
        return {
            'status': 'ok',
            'message': 'Placement Portal is running',
            'database': 'connected'
        }, 200


    @app.route('/uploads/resumes/<filename>')
    @jwt_required()
    def uploaded_resume(filename):
        user_id = int(get_jwt_identity())
        role = get_jwt().get('role')

        # Admin: full access
        if role == 'admin':
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

        # Student: only own resume
        if role == 'student':
            student = Student.query.filter_by(user_id=user_id).first()
            if student and student.resume_url and student.resume_url.endswith('/' + filename):
                return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            return jsonify({'error': 'Unauthorized'}), 403

        # Company: resumes of students who applied to this company's jobs
        if role == 'company':
            company = Company.query.filter_by(user_id=user_id).first()
            if not company:
                return jsonify({'error': 'Company not found'}), 404

            apps = (Application.query
                    .join(JobPosition, Application.job_position_id == JobPosition.id)
                    .filter(JobPosition.company_id == company.id)
                    .all())
            student_ids = {a.student_id for a in apps}
            if not student_ids:
                return jsonify({'error': 'Unauthorized'}), 403

            students = Student.query.filter(Student.id.in_(student_ids)).all()
            allowed_filenames = {
                s.resume_url.split('/')[-1] for s in students if s.resume_url
            }

            if filename in allowed_filenames:
                return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({'error': 'Unauthorized'}), 403


    @app.route('/uploads/photos/<filename>')
    def uploaded_photo(filename):
        return send_from_directory(app.config['PHOTO_FOLDER'], filename)


    print("\n Flask app initialized successfully!")
    print("App is ready for requests\n")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)