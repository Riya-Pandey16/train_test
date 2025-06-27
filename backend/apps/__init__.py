from flask import Flask, jsonify, render_template, send_from_directory
from .extensions import db, migrate, jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from datetime import timedelta
from flask_socketio import SocketIO
from flask_cors import CORS
from apps.msg.routes import msg_bp
from apps.Sessions.routes import session_bp
from flask_socketio import SocketIO




socketio = SocketIO(cors_allowed_origins="*")


def create_app(static_folder=None):
    app = Flask(
        __name__,
        static_folder=static_folder or "static",
        template_folder="templates",
        
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER = 'static/uploads'

    

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uniconnect.db'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # ✅ use 'app', not 'apps'
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context():
        from . import models

    # ✅ imports (assuming you're in apps folder)
    from .auth.routes import auth_bp
    from .posts.routes import posts_bp
    from .profile.routes import profile_bp
    from .admin.routes import admin_bp
    from .Sessions.routes import session_bp
    from apps.msg.routes import msg_bp
    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(session_bp)
    app.register_blueprint(msg_bp, url_prefix='/chat')
    

    @app.route('/default-avatar.png')
    def serve_default_avatar():
       return send_from_directory('static', 'default-avatar.png')




    
    

    return app
    
