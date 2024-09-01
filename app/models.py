from app import db
from flask_login import UserMixin

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
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(128))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<StudySession {self.title}>'