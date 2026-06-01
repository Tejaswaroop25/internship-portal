from datetime import datetime
from backend.models import db

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # 'Pending', 'Reviewed', 'Accepted', 'Rejected'
    cover_letter = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Application student_id={self.student_id} internship_id={self.internship_id} status={self.status}>'
