
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, random

from flask_migrate import Migrate 

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    random.seed(0)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Important: Set to False

    db.init_app(app)
    migrate = Migrate(app, db)
    
    from .views import app_views
    from .prediction import prediction
    from .messages import messages

    app.register_blueprint(prediction, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')
    app.register_blueprint(app_views, url_prefix='')

    from .models import Messages, User  # Import User model

    with app.app_context():  # Use app context for initial database creation
        if not os.path.exists('website/' + DB_NAME):
            db.create_all()  # Create all tables if the database file doesn't exist
        else:  # Database exists, check for tables
            try:
                # Attempt a simple query to check if the User table exists.
                User.query.first()  # Or any other query against a model
            except Exception as e: # if table does not exist
                print(f"Database tables might be missing: {e}")
                db.create_all()  # Create tables if they don't seem to exist

    return app


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)

