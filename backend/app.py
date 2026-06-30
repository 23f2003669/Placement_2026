from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS
from config import get_config
from models import db
from database import init_db
from datetime import timedelta
from celery_config import celery_app
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

    # Make celery app work with Flask
    class ContextTask(celery_app.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery_app.Task = ContextTask
    
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
    def uploaded_resume(filename):

        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename
        )


    print("\n Flask app initialized successfully!")
    print("App is ready for requests\n")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)