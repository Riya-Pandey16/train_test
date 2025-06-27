from flask import Blueprint, request, jsonify
from apps.models import User, Post
from apps import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.auth.decorators import admin_required


admin_bp = Blueprint('admin', __name__)

# ----------------------------
# Admin: Get All Users
# ----------------------------
@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    if not current_user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    users = User.query.all()
    result = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'branch': user.branch,
        'year': user.year,
        'is_admin': user.is_admin
    } for user in users]

    return jsonify(result), 200

# ----------------------------
# Admin: Delete User by ID
# ----------------------------
@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    if not current_user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
