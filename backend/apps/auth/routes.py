from flask import Blueprint, request, jsonify
from apps.models import User
from apps.extensions import db  # ✅ Correct
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

# ----------------------------
# Register Route
# ----------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'branch', 'year']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Unique checks
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        branch=data['branch'],
        year=data['year'],
        is_admin=data.get('is_admin', False)
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"msg": "Auth blueprint working"})


# ----------------------------
# Login Route
# ----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # ✅ Auto-create profile if it doesn't exist
        from apps.models import Profile  # adjust import as per your structure
        existing_profile = Profile.query.filter_by(user_id=user.id).first()
        if not existing_profile:
            default_profile = Profile(
                name=user.username or "New User",  # fallback if no username
                branch=user.branch or "",  # if available from User model
                year=user.year or "",
                skills="",
                user_id=user.id
            )
            db.session.add(default_profile)
            db.session.commit()

        # Token data (you can expand this if needed)
        token_data = {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'branch': user.branch,
            'year': user.year
        }
        access_token = create_access_token(identity=user.id, additional_claims=token_data)
        return jsonify(access_token=access_token), 200

    return jsonify({'error': 'Invalid credentials'}), 401



