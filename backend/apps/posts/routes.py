from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import db, Post, User
from werkzeug.utils import secure_filename
import os


posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')



UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'ppt', 'pptx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@posts_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    post_list = []

    for post in posts:
        user = User.query.get(post.user_id)
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "timestamp": post.timestamp.isoformat(),
            "file_url": post.file_url,
            "user_id": post.user_id,
            "author": {
                "id": user.id,
                "name": user.username,
                "branch": user.branch,
                "year": user.year
            }
        }
        post_list.append(post_data)

    return jsonify(post_list), 200


@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    try:
        user_id = get_jwt_identity()
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('file')

        file_url = None
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            file_url = f'/posts/uploads/{filename}'


        new_post = Post(
            title=title,
            content=content,
            user_id=user_id,
            file_url=file_url
        )
        db.session.add(new_post)
        db.session.commit()

        return jsonify({"msg": "Post created", "post_id": new_post.id}), 201
    except Exception as e:
        print("Error in create_post():", e)
        return jsonify({"msg": "Failed to create post", "error": str(e)}), 500
    
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    user = User.query.get(user_id)

    if post.user_id != user_id and not user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted"}), 200



@posts_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploaded_file(filename):
    directory = os.path.join(os.getcwd(), 'static', 'uploads')
    return send_from_directory(directory, filename)



    # Check if current user is admin or post owner
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if post.user_id != user_id and not user.is_admin:
        return jsonify({'error': 'Forbidden: You can only delete your own posts'}), 403

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post', 'details': str(e)}), 500
