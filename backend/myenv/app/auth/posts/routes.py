from flask import Blueprint, request, jsonify
from app.models import Post, db

post_bp = Blueprint('posts', __name__)

@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': p.id, 'content': p.content, 'user_id': p.user_id} for p in posts])

@post_bp.route('/', methods=['POST'])
def create_post():
    data = request.json
    post = Post(content=data['content'], user_id=data['user_id'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created'}), 201
