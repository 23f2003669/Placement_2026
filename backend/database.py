import os
from models import db, User, UserRole, Admin
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_db(app):
    """
    Initialize database:
    1. Create all tables
    2. Create admin user if doesn't exist
    """
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print(" Database tables created successfully!")

        print("\nChecking for admin user...")
        admin_user = User.query.filter_by(username='admin').first()

        if not admin_user:
            print("Admin user not found. Creating...")

            # Get credentials from .env file (secure way)
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@placement.edu')
            admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123!Secure')

            admin_user = User(
                username='admin',
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role=UserRole.ADMIN.value,
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()

            admin_profile = Admin(
                user_id=admin_user.id,
                name='Institute Admin',
                designation='Placement Cell Head'
            )
            db.session.add(admin_profile)
            db.session.commit()

            print(" Admin user created successfully!")
            print(f"  Email: {admin_email}")
            print("  Password: Check .env file (ADMIN_PASSWORD)")
        else:
            print(" Admin user already exists!")


def reset_db(app):
    """
    Drop all tables and recreate them (WARNING: Deletes all data!)
    """
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("All tables dropped!")
        print("Now initializing database again...")
        init_db(app)
