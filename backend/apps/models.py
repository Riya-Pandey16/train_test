# app/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from apps.extensions import db
from flask_login import UserMixin
from datetime import datetime


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(100))
    year = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', back_populates='author')
    profile_picture = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String(200))  # <== ADD THIS if missing
    # ✅ Fix: Correct foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # ✅ Optional: relationship to access post.author
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            "timestamp": self.timestamp.isoformat(),
            'author_id': self.author_id,
            'file_url': self.file_url
        }

    author = db.relationship('User', back_populates='posts')
    

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    year = db.Column(db.String(50))
    skills = db.Column(db.String(300))
    About = db.Column(db.String(500))  # Add this line for the About field
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


    # ✅ Session model definition
class Session(db.Model):
    __tablename__ = 'Session'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String(255), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Add this

    user = db.relationship('User', backref='sessions')

    def __repr__(self):
        return f"<session {self.topic} at {self.time}>"
    



class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    messages = db.relationship('Message', back_populates='room', cascade="all, delete-orphan")
    participants = db.relationship('Participant', back_populates='room', cascade="all, delete-orphan")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=True)

    content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String, nullable=True)
    file_type = db.Column(db.String, nullable=True)
    deleted_for_sender = db.Column(db.Boolean, default=False)
    deleted_for_receiver = db.Column(db.Boolean, default=False)

    room = db.relationship('ChatRoom', back_populates='messages')
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])


class MessageReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reaction = db.Column(db.String(10), nullable=False)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)

    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='participants')
    room = db.relationship('ChatRoom', back_populates='participants')