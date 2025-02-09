from . import db 
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class Messages(db.Model):
	"""model for stocking the messages from contact us"""
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	name = db.Column(db.String(150))
	email = db.Column(db.String(150))
	messages = db.Column(db.String(10000))

	def __str__(self):

		return self.name
	
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Added username
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>" 