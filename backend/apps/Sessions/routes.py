from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import Session
from apps.extensions import db
from datetime import datetime


session_bp = Blueprint('session', __name__)

@session_bp.route('/session/create', methods=['POST'])
@jwt_required()
def create_session():
    data = request.get_json()

    topic = data.get('topic')
    time_str = data.get('time')
    link = data.get('link')

    if not topic or not time_str or not link:
        return jsonify({'error': 'Missing topic, time, or link'}), 400

    try:
        time_obj = datetime.fromisoformat(time_str)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400

    user_id = get_jwt_identity()

    new_session = Session(topic=topic, time=time_obj, link=link, user_id=user_id)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        'id': new_session.id,
        'topic': new_session.topic,
        'time': new_session.time.isoformat(),
        'link': new_session.link,
        'user_id': new_session.user_id
    }), 201

@session_bp.route('/session/all', methods=['GET'])
@jwt_required()
def get_sessions():
    sessions = Session.query.order_by(Session.time.asc()).all()
    session_list = [{
        'id': s.id,
        'topic': s.topic,
        'time': s.time.isoformat(),
        'link': s.link,
        'user_id': s.user_id  # ✅ Add this line
    } for s in sessions]
    return jsonify(session_list), 200


@session_bp.route('/session/delete/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    current_user_id = get_jwt_identity()

    if session.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'}), 200

