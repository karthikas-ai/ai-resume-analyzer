"""
Database models for AI Resume Analyzer & Career Coach.

Tables:
    User      - registered users
    Resume    - uploaded resume files + extracted text
    Analysis  - AI/rule-based analysis results tied to a resume
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship(
        "Resume", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    stored_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf / docx
    raw_text = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    analyses = db.relationship(
        "Analysis", backref="resume", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Resume {self.filename}>"


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)

    overall_score = db.Column(db.Integer, nullable=False)          # 0-100
    ats_score = db.Column(db.Integer, nullable=False)               # 0-100
    predicted_role = db.Column(db.String(150))
    matched_skills = db.Column(db.Text)      # JSON-encoded list
    missing_skills = db.Column(db.Text)      # JSON-encoded list
    learning_recommendations = db.Column(db.Text)  # JSON-encoded list
    interview_questions = db.Column(db.Text)        # JSON-encoded list
    ai_suggestions = db.Column(db.Text)      # Granite / fallback generated text
    ats_issues = db.Column(db.Text)          # JSON-encoded list of ATS problems
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Analysis resume={self.resume_id} score={self.overall_score}>"
