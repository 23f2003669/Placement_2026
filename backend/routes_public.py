from flask import Blueprint, jsonify
from models import Student, Company, JobPosition, Placement

public_bp = Blueprint('public', __name__, url_prefix='/api/public')


@public_bp.route('/stats', methods=['GET'])
def public_stats():
    """Aggregated, non-sensitive stats for the public landing page (no auth)."""
    try:
        total_students = Student.query.count()
        total_companies = Company.query.filter_by(approval_status='approved').count()
        total_drives = JobPosition.query.filter_by(status='approved').count()
        total_placements = Placement.query.count()

        placements = Placement.query.all()
        highest = max([p.salary for p in placements if p.salary], default=0)

        return jsonify({
            'success': True,
            'stats': {
                'students_placed': total_placements,
                'total_students': total_students,
                'recruiters': total_companies,
                'active_drives': total_drives,
                'highest_package': highest
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
