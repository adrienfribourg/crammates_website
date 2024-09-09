from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    university = db.Column(db.String(150), nullable=True)
    courses = db.Column(db.String(300), nullable=True)
    sessions = db.relationship('StudySession', backref='creator', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(128), nullable=False)  # Changed 'title' to 'topic' to match form field
    date = db.Column(db.Date, nullable=False)  # Ensure it's a date to match input
    time = db.Column(db.Time, nullable=False)  # Added a separate time field for better control
    location = db.Column(db.String(128), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<StudySession {self.topic}>'

    @staticmethod
    def get_upcoming_sessions():
        """Retrieve all upcoming study sessions ordered by date and time."""
        return StudySession.query.filter(StudySession.date >= datetime.utcnow()).order_by(StudySession.date, StudySession.time).all()
