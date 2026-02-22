from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'alumni', 'students'
    is_approved = db.Column(db.Boolean, default = False) #use for approving alumni
    resume_file = db.Column(db.String(100), nullable = True) #optional
    #define relationships
    sessions = db.relationship('Session', backref = 'mentor', lazy = True)
    applications = db.relationship('Application', backref = 'student',lazy = True)



class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(400))
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    is_approved = db.Column(db.Boolean, default = False)

    #relationship
    applications = db.relationship('Application', backref = 'session', lazy = True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable = False)
    status = db.Column(db.String(20), default = 'Pending') #Accepted, Rejected


