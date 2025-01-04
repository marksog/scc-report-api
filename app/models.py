from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reports = db.relationship('Report', backref='user', lazy=True)

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    prayers = db.relationship('Prayer', backref='report', lazy=True, cascade="all, delete-orphan")
    studies = db.relationship('Study', backref='report', lazy=True, cascade="all, delete-orphan")
    outreaches = db.relationship('Outreach', backref='report', lazy=True, cascade="all, delete-orphan")
    followups = db.relationship('Followup', backref='report', lazy=True, cascade="all, delete-orphan")

class Prayer(db.Model):
    __tablename__ = 'prayers'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    prayer_chain_start = db.Column(db.Time, nullable=True)
    prayer_chain_end = db.Column(db.Time, nullable=True)
    prayer_group_day = db.Column(db.String(20), nullable=True)
    prayer_group_start = db.Column(db.Time, nullable=True)
    prayer_group_end = db.Column(db.Time, nullable=True)

class Study(db.Model):
    __tablename__ = 'studies'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    study_date = db.Column(db.Date, nullable=True)
    study_content = db.Column(db.Text, nullable=True)

class Outreach(db.Model):
    __tablename__ = 'outreaches'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    total_reached = db.Column(db.Integer, default=0)
    already_saved = db.Column(db.Integer, default=0)
    saved = db.Column(db.Integer, default=0)
    saved_and_filled = db.Column(db.Integer, default=0)
    already_saved_and_filled = db.Column(db.Integer, default=0)
    healed = db.Column(db.Integer, default=0)
    outreach_comments = db.Column(db.Text, nullable=True)

class Followup(db.Model):
    __tablename__ = 'followups'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    followup_date = db.Column(db.Date, nullable=True)
    followup_persons = db.Column(db.String(255), nullable=True)
    followup_details = db.Column(db.Text, nullable=True)