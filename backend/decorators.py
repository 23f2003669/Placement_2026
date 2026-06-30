from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from models import User

# ============================================
# DECORATOR 1: @login_required
# ============================================

def login_required(fn):
    """
    Decorator to check if user is logged in (has valid JWT token)
    Usage: @login_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({'error': 'Please login first'}), 401
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
    return wrapper


# ============================================
# DECORATOR 2: @role_required
# ============================================

def role_required(required_role):
    """
    Decorator to check if user has required role
    Usage: @role_required('admin')
           @role_required('student')
           @role_required('company')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Get JWT claims (contains role and email)
                claims = get_jwt()
                user_role = claims.get('role')
                
                # Check if user has required role
                if user_role != required_role:
                    return jsonify({
                        'error': f'Access Denied! Only {required_role} can access this'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Unauthorized access'}), 403
        return wrapper
    return decorator


# ============================================
# DECORATOR 3: @any_role_required
# ============================================

def any_role_required(*allowed_roles):
    """
    Decorator to check if user has any of the allowed roles
    Usage: @any_role_required('admin', 'company')
           This allows both admin and company
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Get JWT claims
                claims = get_jwt()
                user_role = claims.get('role')
                
                # Check if user role is in allowed roles
                if user_role not in allowed_roles:
                    return jsonify({
                        'error': f'Access Denied! Only {", ".join(allowed_roles)} can access this'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Unauthorized access'}), 403
        return wrapper
    return decorator