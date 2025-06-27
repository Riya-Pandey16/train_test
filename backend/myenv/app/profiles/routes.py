from flask import Blueprint, jsonify
from app.models import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'message': 'User not found'}), 404
