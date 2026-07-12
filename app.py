"""
AI Resume Analyzer & Career Coach
==================================
Main Flask application entry point.

Run with:
    python app.py

IBM SkillsBuild / Edunet Foundation Final Project.
"""
import os
import json
import uuid
from datetime import datetime

from flask import (
    Flask, render_template, redirect, url_for, request, flash,
    jsonify, send_file, abort
)
from flask_login import login_required, current_user
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from backend import db, login_manager
from backend.models import User, Resume, Analysis
from backend.auth import auth_bp
from backend.resume_parser import extract_resume_text, allowed_file, ResumeParseError
from backend.analyzer import full_local_analysis
from backend.ai_service import (
    generate_resume_improvement_suggestions,
    generate_interview_questions,
    generate_career_coach_advice,
    is_granite_configured,
)
from backend.report_generator import build_analysis_pdf

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    db_url = os.getenv("DATABASE_URL", "sqlite:///database/resume_analyzer.db")
    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        rel_path = db_url.replace("sqlite:///", "")
        db_url = "sqlite:///" + os.path.join(BASE_DIR, rel_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))
    max_mb = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5"))
    app.config["MAX_CONTENT_LENGTH"] = max_mb * 1024 * 1024

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "static", "reports"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------
    @app.errorhandler(413)
    def file_too_large(e):
        flash("File is too large. Maximum upload size is 5 MB.", "danger")
        return redirect(url_for("main.upload")), 413

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", code=500, message="Something went wrong on our end."), 500

    # ------------------------------------------------------------------
    # Main blueprint (routes)
    # ------------------------------------------------------------------
    from flask import Blueprint
    main_bp = Blueprint("main", __name__)

    @main_bp.route("/")
    def index():
        return render_template("index.html")

    @main_bp.route("/dashboard")
    @login_required
    def dashboard():
        resumes = (
            Resume.query.filter_by(user_id=current_user.id)
            .order_by(Resume.uploaded_at.desc())
            .all()
        )
        latest_analysis = None
        if resumes:
            latest_analysis = (
                Analysis.query.filter_by(resume_id=resumes[0].id)
                .order_by(Analysis.created_at.desc())
                .first()
            )
        return render_template(
            "dashboard.html",
            resumes=resumes,
            latest_analysis=latest_analysis,
            granite_configured=is_granite_configured(),
        )

    @main_bp.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        if request.method == "POST":
            file = request.files.get("resume_file")
            if not file or file.filename == "":
                flash("Please choose a resume file to upload.", "danger")
                return redirect(url_for("main.upload"))

            if not allowed_file(file.filename):
                flash("Unsupported file type. Please upload a PDF or DOCX file.", "danger")
                return redirect(url_for("main.upload"))

            original_name = secure_filename(file.filename)
            ext = original_name.rsplit(".", 1)[1].lower()
            unique_name = f"{current_user.id}_{uuid.uuid4().hex[:10]}_{original_name}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)

            try:
                file.save(save_path)
                raw_text = extract_resume_text(save_path)
            except ResumeParseError as exc:
                if os.path.exists(save_path):
                    os.remove(save_path)
                flash(f"Could not process resume: {exc}", "danger")
                return redirect(url_for("main.upload"))
            except Exception as exc:
                flash(f"Unexpected error while uploading: {exc}", "danger")
                return redirect(url_for("main.upload"))

            resume = Resume(
                user_id=current_user.id,
                filename=original_name,
                stored_path=save_path,
                file_type=ext,
                raw_text=raw_text,
            )
            db.session.add(resume)
            db.session.commit()

            flash("Resume uploaded successfully! Running analysis...", "success")
            return redirect(url_for("main.analyze", resume_id=resume.id))

        return render_template("upload.html")

    @main_bp.route("/analyze/<int:resume_id>")
    @login_required
    def analyze(resume_id):
        resume = Resume.query.get_or_404(resume_id)
        if resume.user_id != current_user.id:
            abort(403)

        # Run deterministic local analysis
        result = full_local_analysis(resume.raw_text, resume.filename)

        # AI-generated (Granite or fallback) additions
        ai_suggestions = generate_resume_improvement_suggestions(
            resume.raw_text, result["missing_skills"], result["ats_issues"]
        )
        interview_qs = generate_interview_questions(
            result["predicted_role"], result["matched_skills"]
        )
        coach_advice = generate_career_coach_advice(
            result["predicted_role"], result["overall_score"], result["missing_skills"]
        )

        analysis = Analysis(
            resume_id=resume.id,
            overall_score=result["overall_score"],
            ats_score=result["ats_score"],
            predicted_role=result["predicted_role"],
            matched_skills=json.dumps(result["matched_skills"]),
            missing_skills=json.dumps(result["missing_skills"]),
            learning_recommendations=json.dumps(result["learning_recommendations"]),
            interview_questions=json.dumps(interview_qs),
            ai_suggestions=ai_suggestions + "\n\nCareer Coach Note: " + coach_advice,
            ats_issues=json.dumps(result["ats_issues"]),
        )
        db.session.add(analysis)
        db.session.commit()

        return redirect(url_for("main.analysis_result", analysis_id=analysis.id))

    @main_bp.route("/analysis/<int:analysis_id>")
    @login_required
    def analysis_result(analysis_id):
        analysis = Analysis.query.get_or_404(analysis_id)
        resume = Resume.query.get_or_404(analysis.resume_id)
        if resume.user_id != current_user.id:
            abort(403)

        data = {
            "matched_skills": json.loads(analysis.matched_skills),
            "missing_skills": json.loads(analysis.missing_skills),
            "learning_recommendations": json.loads(analysis.learning_recommendations),
            "interview_questions": json.loads(analysis.interview_questions),
            "ats_issues": json.loads(analysis.ats_issues),
        }
        return render_template(
            "analysis.html",
            analysis=analysis,
            resume=resume,
            data=data,
            granite_configured=is_granite_configured(),
        )

    @main_bp.route("/download-report/<int:analysis_id>")
    @login_required
    def download_report(analysis_id):
        analysis = Analysis.query.get_or_404(analysis_id)
        resume = Resume.query.get_or_404(analysis.resume_id)
        if resume.user_id != current_user.id:
            abort(403)

        analysis_dict = {
            "predicted_role": analysis.predicted_role,
            "overall_score": analysis.overall_score,
            "ats_score": analysis.ats_score,
            "matched_skills": json.loads(analysis.matched_skills),
            "missing_skills": json.loads(analysis.missing_skills),
            "ats_issues": json.loads(analysis.ats_issues),
            "learning_recommendations": json.loads(analysis.learning_recommendations),
            "ai_suggestions": analysis.ai_suggestions,
            "interview_questions": json.loads(analysis.interview_questions),
        }

        reports_dir = os.path.join(BASE_DIR, "static", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        pdf_path = os.path.join(reports_dir, f"report_{analysis.id}.pdf")
        build_analysis_pdf(pdf_path, current_user.full_name, resume.filename, analysis_dict)

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"Resume_Analysis_Report_{analysis.id}.pdf",
        )

    @main_bp.route("/api/resume/<int:resume_id>/delete", methods=["POST"])
    @login_required
    def delete_resume(resume_id):
        resume = Resume.query.get_or_404(resume_id)
        if resume.user_id != current_user.id:
            abort(403)
        if os.path.exists(resume.stored_path):
            os.remove(resume.stored_path)
        db.session.delete(resume)
        db.session.commit()
        flash("Resume deleted.", "info")
        return redirect(url_for("main.dashboard"))

    @main_bp.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "time": datetime.utcnow().isoformat(),
            "granite_configured": is_granite_configured(),
        })

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5000)
