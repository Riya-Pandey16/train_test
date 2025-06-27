from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    CORS(app)
    db.init_app(app)

    from .auth.routes import auth_bp
    from .posts.routes import post_bp
    from .profile.routes import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    with app.app_context():
        db.create_all()

    return app
