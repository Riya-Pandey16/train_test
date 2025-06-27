from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.extensions import db
from apps.models import Profile, User    # adjust imports based on your structure
from werkzeug.utils import secure_filename
import os


profile_bp = Blueprint('profile', __name__)

# Get all profiles
@profile_bp.route('/profiles', methods=['GET'])
@jwt_required()
def get_all_profiles():
    profiles = Profile.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "branch": p.branch,
        "year": p.year,
        "skills": p.skills,
        "About": p.About,
    } for p in profiles]), 200

# Get my own profile
@profile_bp.route('/profile/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile or not user:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify({
        "id": profile.id,
        "name": profile.name,
        "branch": profile.branch,
        "year": profile.year,
        "skills": profile.skills,
        "About": profile.About,
        "is_admin": user.is_admin ,
        "profile_picture": user.profile_picture,
    }), 200

# Get profile by ID
@profile_bp.route('/profile/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_profile_by_id(id):
    profile = Profile.query.get(id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify({
        "id": profile.id,
        "name": profile.name,
        "branch": profile.branch,
        "year": profile.year,
        "skills": profile.skills,
        "About": profile.About,
        
    }), 200

# Update own profile
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/profile/me', methods=['PUT'])
@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile or not user:
        return jsonify({"error": "Profile not found"}), 404

    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            user.profile_picture = f"/{UPLOAD_FOLDER}/{filename}"

    if request.is_json:
        data = request.get_json()
    else:
        data = request.form  # for multipart form

    profile.name = data.get('name', profile.name)
    profile.branch = data.get('branch', profile.branch)
    profile.year = data.get('year', profile.year)
    profile.skills = data.get('skills', profile.skills)
    profile.About = data.get('About', profile.About)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200


# Upload profile picture
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/upload-profile-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    if 'picture' not in request.files:
        return jsonify({"error": "No picture file provided"}), 400

    file = request.files['picture']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)  # Ensure folder exists
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        file_url = f'/profile/uploads/{filename}'

        # Save relative path in DB
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        user.profile_picture = f'/static/uploads/{filename}'
        db.session.commit()

        return jsonify({"message": "Profile picture uploaded", "profile_picture": user.profile_picture}), 200
    
@profile_bp.route('/profile/uploads/<path:filename>', methods=['GET'])
def serve_profile_picture(filename):
    upload_folder = os.path.join(current_app.root_path, 'profile', 'uploads')
    return send_from_directory(upload_folder, filename)
