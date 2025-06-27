from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from apps.extensions import db
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_socketio import emit, join_room
from apps.models import db, User, Message, MessageReaction
from apps.extensions import socketio
from flask_socketio import disconnect

msg_bp= Blueprint('msg', __name__, url_prefix='/chat')

#UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")


# def allowed_file(f): return "." in f and f.rsplit(".",1)[1].lower() in ALLOWED

@msg_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    me = get_jwt_identity()
    users = User.query.filter(User.id != me).all()
    return jsonify([{"id":u.id,"name":u.username,"profile_picture":u.profile_picture} for u in users])

@msg_bp.route('/messages/<int:rid>', methods=['GET'])
@jwt_required()
def get_msgs(rid):
    me = get_jwt_identity()
    msgs = Message.query.filter(
        ((Message.sender_id == me)&(Message.receiver_id==rid)&(Message.deleted_for_sender==False))|
        ((Message.sender_id == rid)&(Message.receiver_id==me)&(Message.deleted_for_receiver==False))
    ).order_by(Message.timestamp).all()
    return jsonify([{
        "id":m.id, "sender_id":m.sender_id, "receiver_id":m.receiver_id,
        "content":m.content, "file":m.file_url, "timestamp":m.timestamp,
        "reactions":[r.reaction for r in MessageReaction.query.filter_by(message_id=m.id)]
    } for m in msgs])



@msg_bp.route('/delete/<int:mid>', methods=['POST'])
@jwt_required()
def delete_message(mid):
    mode = request.json.get('mode')
    uid = get_jwt_identity()
    msg = Message.query.get(mid)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    if mode == "self":
        if msg.sender_id == uid:
            msg.deleted_for_sender = True
        elif msg.receiver_id == uid:
            msg.deleted_for_receiver = True
        else:
            return jsonify({"error": "Unauthorized"}), 403
    elif mode == "everyone":
        if msg.sender_id != uid:
            return jsonify({"error": "Only sender can delete for everyone"}), 403
        msg.content = "[Message deleted]"
        msg.file_url = None
        msg.reactions.clear()
        msg.deleted_for_sender = True
        msg.deleted_for_receiver = True
    else:
        return jsonify({"error": "Invalid mode"}), 400

    db.session.commit()
    return jsonify({"success": True})

@msg_bp.route('/react', methods=['POST'])
@jwt_required()
def react():
    data = request.get_json()
    uid = get_jwt_identity()
    msg_id = data.get("message_id")
    reaction = data.get("reaction")

    if not msg_id or not reaction:
        return jsonify({"error": "Missing data"}), 400

    # Avoid duplicate reactions by same user
    existing = MessageReaction.query.filter_by(message_id=msg_id, user_id=uid, reaction=reaction).first()
    if not existing:
        new_reaction = MessageReaction(message_id=msg_id, user_id=uid, reaction=reaction)
        db.session.add(new_reaction)
        db.session.commit()

    return jsonify({"success": True})

@socketio.on('join_room')
def join(data):
    user_id = data.get('user_id')
    target_id = data.get('target_id')
    room = f"{min(user_id, target_id)}_{max(user_id, target_id)}"
    join_room(room)
    print(f"User {user_id} joined room {room}")  # Debug log

@socketio.on('send_message')
def handle_send_message(data):
    # FIXED: Remove JWT verification that was causing issues
    # Instead, pass sender_id from frontend or use session
    sender_id = data.get('sender_id')  # Add this to frontend emit
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    file = data.get('file')

    if not receiver_id or not sender_id:
        emit("error", {"message": "Missing sender or receiver ID"})
        return

    msg = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        file_url=file
    )
    db.session.add(msg)
    db.session.commit()

    room = f"{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    print(f"Emitting message to room {room}")  # Debug log
    
    emit('receive_message', {
        "id": msg.id,
        "sender_id": msg.sender_id,
        "receiver_id": msg.receiver_id,
        "content": msg.content,
        "file": msg.file_url,
        "timestamp": str(msg.timestamp),
        "reactions": []
    }, room=room)

@socketio.on('typing')
def handle_typing(data):
    from_id = data.get("from")
    to_id = data.get("to")
    # FIXED: Use the same room format as join_room
    room = f"{min(from_id, to_id)}_{max(from_id, to_id)}"
    emit("user_typing", {"from": from_id}, room=room)

@socketio.on('connect')
def handle_connect():
    # FIXED: Remove JWT verification that disconnects clients
    print("Client connected")  # Simple debug log
    
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")




@msg_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_msg():
    me = get_jwt_identity()
    data = request.get_json()
    m = Message(sender_id=me, receiver_id=data["receiver_id"],
                content=data.get("content"), file_url=data.get("file"))
    db.session.add(m)
    db.session.commit()
    payload = {
        "id": m.id,
        "sender_id": m.sender_id,
        "receiver_id": m.receiver_id,
        "content": m.content,
        "file": m.file_url,
        "timestamp": m.timestamp,
        "reactions": []
    }
    # ✅ Emit to both users
    socketio.emit('receive_message', payload, room=f"user_{me}")
    socketio.emit('receive_message', payload, room=f"user_{data['receiver_id']}")
    return jsonify(payload), 201


    

# Use absolute path to 'uploads' folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'txt', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@msg_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # ✅ Now inside a valid app context
        UPLOAD_FOLDER = os.path.abspath(os.path.join(current_app.root_path, '..', 'uploads'))

        # Create uploads directory if missing
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        try:
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            file_url = f"/chat/uploads/{filename}"
            return jsonify({
                'message': 'File uploaded successfully',
                'file_url': file_url,
                'filename': filename
            }), 200

        except Exception as e:
            print(f"File upload error: {e}")
            return jsonify({'error': 'Server error while saving file'}), 500

    return jsonify({'error': 'File type not allowed'}), 400

@msg_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploaded_file(filename):
    UPLOAD_FOLDER = os.path.abspath(os.path.join(current_app.root_path, '..', 'uploads'))
    return send_from_directory(UPLOAD_FOLDER, filename)

