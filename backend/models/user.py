from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'company', 'admin'
    
    # Student profile fields
    skills = db.Column(db.String(500), nullable=True)  # Comma-separated (e.g. "Python, Flask, React")
    experience = db.Column(db.Text, nullable=True)
    resume_link = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)            # Acts as bio for student and company info for company

    # Company specific fields
    company_name = db.Column(db.String(100), nullable=True)
    company_website = db.Column(db.String(200), nullable=True)

    # Relationships
    internships = db.relationship('Internship', backref='company', lazy=True, cascade="all, delete-orphan")
    applications = db.relationship('Application', backref='student', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
