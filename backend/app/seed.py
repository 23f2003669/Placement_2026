from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import User
from app.config import Config


def seed_admin():
    app = create_app()
    with app.app_context():
        db.create_all()

        existing_admin = User.query.filter_by(role="admin").first()
        if existing_admin:
            print(f"Admin already exists: {existing_admin.email}")
            return

        admin = User(
            email=Config.ADMIN_EMAIL,
            password_hash=generate_password_hash(Config.ADMIN_PASSWORD),
            role="admin",
            is_active_flag=True,
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created: {Config.ADMIN_EMAIL} / {Config.ADMIN_PASSWORD}")


if __name__ == "__main__":
    seed_admin()