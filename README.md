# 🧭 ResumeIQ — AI Resume Analyzer & Career Coach

> **IBM SkillsBuild / Edunet Foundation — Final Project Submission**

An end-to-end web application that analyzes resumes (PDF/DOCX), scores them
against ATS (Applicant Tracking System) standards, detects skills, predicts
the best-fit career role, and uses **IBM watsonx.ai (Granite)** to generate
personalized improvement suggestions and interview questions.

---

# 📸 Application Screenshots

## 🏠 Home Page

The landing page introduces ResumeIQ, highlighting AI-powered resume analysis, ATS compatibility scoring, career prediction, and IBM watsonx.ai integration.

![Home Page](screenshots/home page.png)

---

## 👤 User Login Page

Users can create a secure account using their name, email address, and password. Passwords are securely hashed before being stored.

![User Login Page](screenshots/User Login Page .png)

---

## 📊 User Dashboard

After logging in, users are welcomed with a personalized dashboard where they can upload resumes, view previous analyses, and track ATS scores.

![Dashboard](screenshots/dashboard page.png)

---

## 📄 Resume Upload

Users can upload PDF or DOCX resumes for analysis. The application extracts resume content and starts the AI-powered evaluation.

![Resume Upload](screenshots/upload page.png)

---

## 🤖 AI Resume Analysis

The system analyzes the uploaded resume and provides:

- Overall Resume Score
- ATS Compatibility Score
- Predicted Career Role
- Matched Skills
- Missing Skills
- Learning Recommendations
- AI Improvement Suggestions
- Practice Interview Questions
- Downloadable PDF Report

Powered by *IBM watsonx.ai Granite Foundation Model*.

![Analysis Results](screenshots/analysis page.png)


## 📌 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Architecture](#-project-architecture)
4. [Folder Structure](#-folder-structure)
5. [Installation Guide](#-installation-guide)
6. [IBM watsonx.ai Setup](#-ibm-watsonxai-setup)
7. [Running the App](#-running-the-app)
8. [API / Route Documentation](#-api--route-documentation)
9. [Sample Test Data](#-sample-test-data)
10. [Deployment Guide](#-deployment-guide)
11. [Future Scope](#-future-scope)
12. [License](#-license)

---

## 🚀 Features

| Category | Feature |
|---|---|
| Auth | User registration & login (hashed passwords, session-based via Flask-Login) |
| Upload | Drag-and-drop resume upload (PDF/DOCX), 5 MB limit |
| Parsing | Robust text extraction (PyPDF2 for PDF, python-docx for Word, including tables) |
| Scoring | Composite **Resume Score (0–100)** — skill coverage, ATS compatibility, section completeness, length |
| ATS Check | Detects missing sections, poor formatting, image-only resumes, length issues |
| Skills | Detects 60+ known technical skills across 8 career tracks |
| Career Prediction | Predicts best-fit role (Data Scientist, Full Stack Developer, AI/ML Engineer, etc.) from skill overlap |
| Gap Analysis | Lists missing skills for the predicted role |
| Learning Paths | Maps missing skills to specific courses/resources |
| AI Suggestions | IBM Granite (or local fallback) generates resume improvement advice |
| Interview Prep | AI-generated, role-specific interview questions |
| Reports | One-click downloadable PDF analysis report (ReportLab) |
| UI/UX | Responsive Bootstrap 5 dashboard, dark/light mode, loading animations, charts |
| Reliability | Full error handling; app runs even without IBM credentials via local AI fallback |

---

## 🛠 Tech Stack

- **Backend:** Python 3.10+, Flask 3, Flask-SQLAlchemy, Flask-Login
- **Frontend:** HTML5, CSS3 (custom design system), JavaScript (vanilla), Bootstrap 5, Chart.js
- **AI:** IBM watsonx.ai — Granite foundation model (`ibm/granite-13b-instruct-v2`)
- **Database:** SQLite
- **File Parsing:** PyPDF2, python-docx
- **Reporting:** ReportLab (PDF generation)

---

## 🏗 Project Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────────┐
│   Browser   │─────▶│   Flask app.py    │─────▶│   SQLite Database   │
│ (Bootstrap, │◀─────│  (routes/views)   │◀─────│ users/resumes/      │
│  Chart.js)  │      └────────┬──────────┘      │ analyses tables     │
└─────────────┘               │                 └────────────────────┘
                               ▼
                 ┌─────────────────────────┐
                 │   backend/ package       │
                 │  ─ resume_parser.py      │  PDF/DOCX → raw text
                 │  ─ analyzer.py           │  rule-based scoring engine
                 │  ─ ai_service.py         │  IBM Granite integration + fallback
                 │  ─ report_generator.py   │  PDF report builder
                 │  ─ auth.py               │  login/register blueprint
                 └────────────┬─────────────┘
                               ▼
                 ┌─────────────────────────┐
                 │   IBM watsonx.ai          │
                 │   Granite Foundation Model │
                 │  (IAM token → text-gen API)│
                 └─────────────────────────┘
```

**Design principle:** the deterministic rule-based engine (`analyzer.py`)
guarantees the app always produces a complete, reproducible score — even
without internet access or IBM credentials. IBM Granite is layered on top
purely for natural-language generation (suggestions, interview questions,
coaching notes), with an automatic, clearly-labeled fallback if the API is
unavailable or unconfigured.

---

## 📁 Folder Structure

```
ai-resume-analyzer/
├── app.py                     # Main Flask entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
│
├── backend/
│   ├── __init__.py            # db + login_manager instances
│   ├── models.py              # User, Resume, Analysis (SQLAlchemy models)
│   ├── auth.py                # /login /register /logout blueprint
│   ├── resume_parser.py       # PDF/DOCX text extraction
│   ├── analyzer.py            # scoring, skills, ATS check, role prediction
│   ├── ai_service.py          # IBM watsonx.ai Granite integration
│   └── report_generator.py    # PDF report builder (ReportLab)
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html             # Hero landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── analysis.html
│   └── error.html
│
├── static/
│   ├── css/style.css          # Full design system (light + dark mode)
│   ├── js/main.js             # Theme toggle, alert auto-dismiss
│   └── reports/               # Generated PDF reports (runtime)
│
├── uploads/                   # Uploaded resumes (runtime, gitignored)
├── database/                  # SQLite database file (runtime, gitignored)
├── sample_resumes/            # Sample PDF/DOCX/TXT resumes for testing
└── docs/
    ├── PROJECT_REPORT.md      # Full IBM SkillsBuild project report
    └── PPT_CONTENT.md         # 12-slide presentation content
```

---

## ⚙️ Installation Guide

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone / extract the project
cd ai-resume-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in SECRET_KEY and (optionally) IBM watsonx.ai credentials

# 5. Run the app
python app.py
```

The app will be available at **http://localhost:5000**

> The database tables and the `uploads/`, `database/`, `static/reports/`
> folders are created automatically on first run.

---

## 🤖 IBM watsonx.ai Setup

1. Sign in to [IBM Cloud](https://cloud.ibm.com) and create/open a **watsonx.ai** project.
2. Generate an **IBM Cloud API Key**: Manage → Access (IAM) → API keys → Create.
3. Copy your **Project ID** from the watsonx.ai project's *Manage* tab.
4. Note your region **endpoint URL** (e.g. `https://us-south.ml.cloud.ibm.com`).
5. Fill these into your `.env` file:

```env
IBM_API_KEY=your-ibm-cloud-api-key-here
IBM_PROJECT_ID=your-watsonx-project-id-here
IBM_URL=https://us-south.ml.cloud.ibm.com
IBM_MODEL_ID=ibm/granite-13b-instruct-v2
```

**No IBM credentials?** No problem — `ai_service.py` automatically detects
missing/placeholder credentials and transparently switches to a rule-based
local AI simulation, so every feature still works end-to-end for demos and
grading.

---

## ▶️ Running the App

```bash
python app.py
```

- Runs on `http://0.0.0.0:5000` by default
- Set `FLASK_DEBUG=False` in `.env` for production-like runs
- Health check: `GET /health` → `{"status": "ok", "granite_configured": true/false}`

---

## 📡 API / Route Documentation

| Route | Method | Auth | Description |
|---|---|---|---|
| `/` | GET | No | Landing / hero page |
| `/register` | GET, POST | No | Create a new account |
| `/login` | GET, POST | No | Log in |
| `/logout` | GET | Yes | Log out |
| `/dashboard` | GET | Yes | User dashboard with resume history & latest score |
| `/upload` | GET, POST | Yes | Upload a resume (PDF/DOCX) |
| `/analyze/<resume_id>` | GET | Yes | Runs full analysis pipeline on a resume, redirects to results |
| `/analysis/<analysis_id>` | GET | Yes | View full analysis results |
| `/download-report/<analysis_id>` | GET | Yes | Download the analysis as a PDF report |
| `/api/resume/<resume_id>/delete` | POST | Yes | Delete a resume and its analyses |
| `/health` | GET | No | JSON health check + Granite config status |

---

## 🧪 Sample Test Data

The `sample_resumes/` folder contains ready-to-upload files for demoing:

- `sample_resume_fullstack.pdf` / `.docx` — targets **Full Stack Developer**
- `sample_resume_datascience.pdf` / `.docx` — targets **Data Scientist**

Upload either file after registering to see the full analysis pipeline in action.

---

## ☁️ Deployment Guide

### Option 1 — Render / Railway / PythonAnywhere (simplest)
1. Push the project to a GitHub repository.
2. Create a new **Web Service**, point it at the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (add `gunicorn` to `requirements.txt` for production)
5. Add environment variables from `.env.example` in the platform's dashboard.

### Option 2 — Docker (optional, add a Dockerfile)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### Production notes
- Switch `SQLALCHEMY_DATABASE_URI` to PostgreSQL/MySQL for multi-user production use.
- Set a strong, random `SECRET_KEY`.
- Set `FLASK_DEBUG=False`.
- Put uploaded files behind proper access control or move to object storage (e.g. IBM Cloud Object Storage) for scale.

---

## 🔮 Future Scope

- Fine-tune a Granite model specifically on resume/job-description pairs for higher-precision role matching.
- Add job-description-matching mode: paste a JD and get a tailored gap analysis.
- LinkedIn profile import.
- Multi-language resume support.
- Resume version history and score-over-time tracking with trend charts.
- Recruiter-facing bulk analysis dashboard.
- Integration with IBM Watson Discovery for deeper document structure analysis.

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

*Built as part of the IBM SkillsBuild & Edunet Foundation internship program.*
