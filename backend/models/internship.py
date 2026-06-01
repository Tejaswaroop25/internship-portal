from datetime import datetime
from backend.models import db

class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.String(500), nullable=False)  # Comma-separated required skills (e.g., "Python, CSS")
    location = db.Column(db.String(100), nullable=False)      # e.g., "Remote", "New York, NY"
    stipend = db.Column(db.String(100), nullable=True)        # e.g., "$1500/month", "Unpaid"
    duration = db.Column(db.String(50), nullable=True)         # e.g., "3 months", "6 months"
    company_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='internship', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Internship {self.title} by Company ID {self.company_id}>'
