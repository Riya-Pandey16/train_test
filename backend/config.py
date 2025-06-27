import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-jwt-secret-key'  # required for JWT
