# Project Report

## AI Resume Analyzer & Career Coach (ResumeIQ)

**Submitted for:** IBM SkillsBuild & Edunet Foundation Internship Program
**Domain:** Artificial Intelligence / Machine Learning — Full Stack Web Application
**Submission Type:** Final Project Report

---

### Student Details

| Field | Detail |
|---|---|
| Name | *(Karthika — fill in full name)* |
| Program | B.E. Computer Science Engineering (AI & ML) |
| Institution | *(Fill in college name)* |
| Domain / Track | IBM SkillsBuild — Artificial Intelligence |
| Project Title | AI Resume Analyzer & Career Coach |
| Mentor / Guide | *(Fill in mentor name)* |

---

## Table of Contents

1. Introduction
2. Problem Statement
3. Literature Review / Existing Solutions
4. Proposed Solution
5. System Requirements
6. System Architecture
7. Technology Stack Justification
8. Module-wise Description
9. Database Design
10. IBM watsonx.ai (Granite) Integration
11. UI/UX Design
12. Testing
13. Results and Screenshots
14. Challenges Faced
15. Future Scope
16. Conclusion
17. References

---

## 1. Introduction

Every year, millions of students and early-career professionals submit
resumes to companies through online portals — the majority of which are
first screened not by a human recruiter, but by an **Applicant Tracking
System (ATS)**. Studies consistently show that a significant fraction of
resumes never reach a human reader simply because of formatting issues,
missing keywords, or an unclear structure. At the same time, many students —
including final-year engineering students preparing for campus placement
drives — do not have consistent access to a professional career coach or
resume reviewer who can give them fast, objective, and actionable feedback.

**ResumeIQ (AI Resume Analyzer & Career Coach)** was built to close this
gap. It is a full-stack web application that allows a user to register,
upload a resume in PDF or DOCX format, and instantly receive:

- A composite **Resume Score (0–100)**
- An **ATS Compatibility Score** with specific, fixable issues listed
- A list of **detected technical skills**
- A **predicted career role** based on skill overlap with real job tracks
- A list of **missing skills** for that role, each mapped to a learning resource
- **AI-generated improvement suggestions**, written by IBM watsonx.ai's
  Granite foundation model (with an automatic local fallback if IBM
  credentials are not configured)
- **AI-generated, role-specific interview questions** to help the candidate
  prepare
- A **downloadable PDF report** summarizing the entire analysis

The project was built end-to-end using Python (Flask), SQLite, Bootstrap 5,
vanilla JavaScript, and IBM watsonx.ai, and is designed to run out-of-the-box
after a single `pip install` and `python app.py`.

---

## 2. Problem Statement

> *"Design and develop an AI-powered web application that analyzes a
> user's resume, evaluates it against ATS standards, identifies skill gaps
> for a predicted career role, and generates personalized, AI-driven
> feedback and interview preparation material — using IBM watsonx.ai."*

### Sub-problems addressed

1. **Text extraction problem** — resumes come in inconsistent formats
   (PDF, DOCX, single-column, multi-column, tables). The system must
   reliably extract clean text regardless of layout.
2. **Scoring problem** — there is no universally agreed single number for
   "resume quality." The system needs a transparent, explainable, and
   reproducible scoring formula.
3. **Skill-gap problem** — a resume in isolation doesn't tell a candidate
   what they are missing *relative to a specific target role*. The system
   must predict the most likely target role and compute the gap.
4. **Feedback-generation problem** — generic feedback ("add more skills")
   is not useful. The system must generate specific, natural-language
   suggestions grounded in the actual resume content — this is where a
   generative AI model like IBM Granite adds real value over pure
   rule-based systems.
5. **Accessibility problem** — the tool must be usable by a non-technical
   student with no setup beyond installing Python packages, and must not
   hard-fail if cloud AI credentials aren't available (e.g., during
   grading/demo without internet).

---

## 3. Literature Review / Existing Solutions

Several categories of existing tools were considered before designing
ResumeIQ:

| Tool Type | Examples | Limitation |
|---|---|---|
| Generic ATS checkers | Jobscan, Resume Worded | Often paywalled; opaque scoring; not tied to a specific AI-generated coaching layer |
| Resume builders | Canva Resume, Novoresume | Focus on templates/design, not analytical feedback |
| Career platforms | LinkedIn "Skill Match" | Requires an active job posting to compare against; not resume-first |
| Generic chatbot review | Pasting resume into a general LLM chat | No persistent scoring, no structured ATS logic, no dashboard/history, no downloadable report |

**Gap identified:** none of the reviewed tools combine (a) a transparent,
rule-based numeric scoring engine, (b) skill-gap analysis against multiple
concrete career tracks, and (c) a generative AI layer (specifically IBM
watsonx.ai Granite) for natural-language coaching — all inside a single,
self-hosted, open web application with user accounts and history. This is
the space ResumeIQ occupies.

---

## 4. Proposed Solution

ResumeIQ is architected as a **hybrid system**:

- A **deterministic rule-based core** (`backend/analyzer.py`) computes the
  Resume Score, ATS Score, matched/missing skills, and predicted role using
  transparent, auditable logic — no black-box dependency. This guarantees
  the application is always fully functional, fast, and reproducible.
- A **generative AI layer** (`backend/ai_service.py`) calls IBM watsonx.ai's
  Granite model to convert the structured analysis into natural, encouraging,
  specific written feedback and interview questions — the part of the
  experience that most benefits from a large language model's fluency.

This hybrid design was a deliberate architectural choice: purely relying on
an LLM for scoring would make results non-reproducible and expensive to
compute at scale, while purely rule-based feedback text reads as robotic and
generic. Combining both gives the best of both worlds.

### High-level user flow

```
Register/Login → Upload Resume (PDF/DOCX) → Text Extraction →
Rule-Based Analysis (score, skills, ATS, role) → IBM Granite
(suggestions, interview Qs, coaching note) → Results Dashboard →
Download PDF Report
```

---

## 5. System Requirements

### Functional Requirements
- FR1: The system shall allow user registration and secure login.
- FR2: The system shall accept resume uploads in PDF and DOCX formats up to 5MB.
- FR3: The system shall extract raw text from the uploaded resume.
- FR4: The system shall compute an overall resume score between 0 and 100.
- FR5: The system shall compute an ATS compatibility score and list specific issues.
- FR6: The system shall detect known technical skills present in the resume.
- FR7: The system shall predict the most likely career role for the candidate.
- FR8: The system shall list missing skills relevant to the predicted role.
- FR9: The system shall recommend learning resources for missing skills.
- FR10: The system shall generate AI-based improvement suggestions via IBM watsonx.ai.
- FR11: The system shall generate role-specific interview questions.
- FR12: The system shall allow the user to download a PDF report of the analysis.
- FR13: The system shall maintain a history of all resumes/analyses per user.

### Non-Functional Requirements
- NFR1: The system shall respond to a resume analysis request within 5 seconds (excluding external AI API latency).
- NFR2: The system shall remain fully functional (with a labeled fallback) if IBM watsonx.ai credentials are not configured.
- NFR3: The UI shall be responsive across desktop, tablet, and mobile viewports.
- NFR4: Passwords shall never be stored in plain text.
- NFR5: The system shall support both light and dark UI themes.

### Hardware/Software Requirements
- Python 3.10+
- 4 GB RAM minimum (development)
- Modern web browser (Chrome, Edge, Firefox)
- Internet connection (only required for live IBM watsonx.ai calls; core app works offline)

---

## 6. System Architecture

The application follows a classic **MVC-inspired Flask architecture**:

- **Model layer:** `backend/models.py` — SQLAlchemy ORM models (`User`, `Resume`, `Analysis`)
- **View layer:** `templates/*.html` — Jinja2-rendered Bootstrap 5 pages
- **Controller layer:** `app.py` + `backend/auth.py` — Flask route handlers (blueprints)
- **Service layer:** `backend/resume_parser.py`, `backend/analyzer.py`, `backend/ai_service.py`, `backend/report_generator.py` — pure business logic, decoupled from Flask so it's independently testable

```
Client (Browser)
      │  HTTP
      ▼
Flask App (app.py)
   ├── auth blueprint  ──▶ models.py ──▶ SQLite
   └── main blueprint
          ├── resume_parser.py   (PDF/DOCX → text)
          ├── analyzer.py        (score, skills, ATS, role)
          ├── ai_service.py      (IBM watsonx.ai Granite / fallback)
          └── report_generator.py (PDF report)
```

This separation of concerns means the analysis engine could be reused in a
CLI tool, a batch job, or a different frontend (e.g., a REST API for a
mobile app) without modification.

---

## 7. Technology Stack Justification

| Layer | Choice | Why |
|---|---|---|
| Backend framework | Flask | Lightweight, explicit, ideal for a project of this scope; easy to explain in a viva |
| ORM | Flask-SQLAlchemy | Avoids raw SQL, provides safe parameterized queries, easy schema evolution |
| Auth | Flask-Login + Werkzeug password hashing | Industry-standard session-based auth pattern, secure password storage (PBKDF2/salted hashes) |
| Database | SQLite | Zero-configuration, file-based, perfect for an academic/demo project; upgrade path to PostgreSQL documented |
| PDF parsing | PyPDF2 | Pure-Python, no external binary dependency, reliable for text-based PDFs |
| DOCX parsing | python-docx | Standard library for reading Word documents including tables |
| PDF report generation | ReportLab | Fine-grained control over layout for a polished, professional report |
| Frontend | Bootstrap 5 + custom CSS | Rapid, responsive UI development with room for a distinctive visual identity |
| Charts | Chart.js | Lightweight, no build step required, renders directly from Jinja-templated data |
| Generative AI | IBM watsonx.ai (Granite) | Required by the IBM SkillsBuild program; enterprise-grade foundation model with a documented REST API |

---

## 8. Module-wise Description

### 8.1 Authentication Module (`backend/auth.py`)
Handles registration (with email format & password-length validation, and
duplicate-email checking) and login (with hashed password verification via
Werkzeug's `check_password_hash`). Uses Flask-Login's session cookies to
persist login state and protect routes with the `@login_required` decorator.

### 8.2 Resume Parser Module (`backend/resume_parser.py`)
Given a file path, dispatches to either `extract_text_from_pdf()` (via
PyPDF2's `PdfReader`, iterating and concatenating page text) or
`extract_text_from_docx()` (via python-docx, reading both paragraphs and
table cells, since many resumes use tables for the skills or contact
section). Raises a custom `ResumeParseError` with a human-readable message
on failure (e.g., scanned image PDFs with no embedded text layer).

### 8.3 Analyzer Module (`backend/analyzer.py`)
The core scoring engine. Key components:

- **`ROLE_SKILLS`**: a curated dictionary mapping 8 career roles (Data
  Scientist, Software Engineer, Full Stack Developer, AI/ML Engineer,
  Business Analyst, Cloud Engineer, Cybersecurity Analyst, UI/UX Designer)
  to their most relevant skill sets.
- **`detect_skills()`**: regex-based, word-boundary-aware matching of
  ~70 known skills against the normalized resume text.
- **`predict_role()`**: computes, for each role, the percentage overlap
  between the candidate's matched skills and that role's skill set, and
  returns the highest-scoring role.
- **`ats_compatibility_check()`**: a rule-based ATS simulator that checks
  for a contact section, a skills section, an education section, an
  experience/projects section, appropriate word count (150–1200 words),
  sufficient bullet-point usage, and image-only submissions — each
  violation deducts points from a starting score of 100.
- **`calculate_overall_score()`**: a weighted composite —
  40% skill coverage + 35% ATS score + 15% section completeness +
  10% length appropriateness.
- **`learning_recommendations()`**: maps missing skills to a curated
  course/resource suggestion.

### 8.4 AI Service Module (`backend/ai_service.py`)
Wraps all communication with IBM watsonx.ai:

1. `_get_iam_token()` exchanges the `IBM_API_KEY` for a short-lived bearer
   token via IBM Cloud's IAM endpoint, caching it until near-expiry.
2. `_call_granite()` sends a prompt to the watsonx.ai
   `/ml/v1/text/generation` endpoint with the Granite model ID, project ID,
   and generation parameters (greedy decoding, max/min tokens, temperature,
   repetition penalty).
3. Three public functions build role- and resume-specific prompts:
   `generate_resume_improvement_suggestions()`,
   `generate_interview_questions()`, and `generate_career_coach_advice()`.
4. Every public function is wrapped so that **any** exception (missing
   credentials, network failure, quota limits) transparently falls back to
   a deterministic, clearly-labeled local suggestion, guaranteeing the
   application never crashes or blocks on the AI call.

### 8.5 Report Generator Module (`backend/report_generator.py`)
Uses ReportLab's `SimpleDocTemplate` and `Platypus` flowables (Paragraph,
Table, ListFlowable) to assemble a structured, styled, one-click PDF export
of the full analysis — candidate name, scores, skills, ATS issues, learning
table, AI suggestions, and interview questions.

### 8.6 Main Application Module (`app.py`)
Wires everything together: Flask app factory (`create_app()`), database
initialization, blueprint registration, file upload handling (with
`secure_filename` and a UUID-based unique filename to prevent collisions
and path traversal), and all page/API routes.

---

## 9. Database Design

### Entity-Relationship Overview

```
User (1) ──────< (many) Resume (1) ──────< (many) Analysis
```

### `users`
| Column | Type | Notes |
|---|---|---|
| id | Integer, PK | |
| full_name | String(150) | |
| email | String(150) | Unique, indexed |
| password_hash | String(255) | Werkzeug salted hash |
| created_at | DateTime | |

### `resumes`
| Column | Type | Notes |
|---|---|---|
| id | Integer, PK | |
| user_id | Integer, FK → users.id | |
| filename | String(255) | Original filename |
| stored_path | String(500) | Path on disk |
| file_type | String(10) | pdf / docx |
| raw_text | Text | Extracted text |
| uploaded_at | DateTime | |

### `analyses`
| Column | Type | Notes |
|---|---|---|
| id | Integer, PK | |
| resume_id | Integer, FK → resumes.id | |
| overall_score | Integer | 0–100 |
| ats_score | Integer | 0–100 |
| predicted_role | String(150) | |
| matched_skills | Text | JSON-encoded list |
| missing_skills | Text | JSON-encoded list |
| learning_recommendations | Text | JSON-encoded list of {skill, resource} |
| interview_questions | Text | JSON-encoded list |
| ai_suggestions | Text | Granite / fallback text |
| ats_issues | Text | JSON-encoded list |
| created_at | DateTime | |

JSON-encoding list/dict fields inside `Text` columns was chosen over
separate join tables to keep the schema simple for an academic project
while still being fully queryable and normalizable if the project is
extended later.

---

## 10. IBM watsonx.ai (Granite) Integration

### Why Granite
IBM's Granite family of foundation models is purpose-built for enterprise
use cases and is directly accessible via the watsonx.ai platform, making it
the natural choice for an IBM SkillsBuild submission. This project uses
`ibm/granite-13b-instruct-v2` for instruction-following text generation.

### Authentication Flow
1. The `.env` file supplies `IBM_API_KEY` and `IBM_PROJECT_ID`.
2. On each (cached) request, the app exchanges the API key for a bearer
   token via IBM Cloud IAM (`POST https://iam.cloud.ibm.com/identity/token`).
3. The bearer token authorizes calls to the watsonx.ai text-generation REST
   endpoint (`POST {IBM_URL}/ml/v1/text/generation?version=2023-05-29`).

### Prompts Used
Three distinct prompt templates were engineered:
1. **Resume improvement suggestions** — includes the resume text (truncated
   to 3000 characters), the missing skills list, and detected ATS issues,
   asking for 5–7 actionable bullet points.
2. **Interview questions** — includes the predicted role and top matched
   skills, asking for 8 realistic technical/behavioral questions.
3. **Career coach advice** — includes the predicted role, overall score,
   and missing skills, asking for a short, honest, motivational note.

### Graceful Degradation
If `IBM_API_KEY`/`IBM_PROJECT_ID` are unset, placeholder values, or the API
call fails for any reason (network, quota, timeout), `ai_service.py`
transparently returns a rule-based fallback string, and the UI displays a
small info banner noting that local fallback suggestions are shown. This
was a deliberate reliability decision so that the project can always be
demonstrated end-to-end, regardless of network access during grading.

---

## 11. UI/UX Design

The interface uses a custom design system layered on top of Bootstrap 5:

- **Palette:** Indigo (`#4F46E5`) primary, Teal (`#0D9488`) for
  success/ATS indicators, Amber (`#F59E0B`) for warnings — chosen to feel
  professional and trustworthy rather than playful.
- **Typography:** Sora (display/headings) paired with Inter (body text) for
  a modern, technical-but-approachable feel.
- **Dark/Light Mode:** implemented via a `data-theme` attribute on the
  `<html>` element and CSS custom properties, toggled by a button in the
  navbar and persisted in `localStorage`.
- **Key screens:**
  - **Hero/Landing page** — value proposition, animated floating score
    cards, feature grid, CTA banner.
  - **Dashboard** — score summary cards, progress bars, resume history table.
  - **Upload page** — drag-and-drop zone with a full-screen loading overlay
    during analysis.
  - **Analysis page** — circular score gauges, a Chart.js bar chart score
    breakdown, skill badges (matched/missing), ATS issue list, learning
    resource table, AI suggestion panel, and numbered interview questions.
- **Accessibility:** semantic HTML, visible focus states via Bootstrap
  defaults, sufficient color contrast in both themes, responsive down to
  narrow mobile viewports.

---

## 12. Testing

| Test | Method | Result |
|---|---|---|
| Python syntax validation | `python -m py_compile` on all backend modules | All files compile without errors |
| Jinja2 template validation | Parsed all templates with `jinja2.Environment.parse()` | All 8 templates parse without syntax errors |
| Resume parsing (DOCX) | Extracted text from a hand-crafted Full Stack Developer sample resume | Text extracted correctly, including all sections |
| Resume parsing (PDF) | Extracted text from a hand-crafted Data Scientist sample resume | Text extracted correctly |
| Analyzer pipeline | Ran `full_local_analysis()` on both sample resumes | Correctly predicted "Full Stack Developer" (score 100) and "Data Scientist" (score 97) respectively, with sensible matched/missing skill lists |
| AI service fallback | Called all 3 AI functions with no IBM credentials configured | Returned well-formed, labeled fallback text with no exceptions |
| PDF report generation | Generated a report from a mock analysis dict | Valid PDF produced (~2.8 KB for the sample) |
| Manual UI walkthrough | Registration → login → upload → analysis → PDF download | Full flow functions as designed |

### Sample Test Output (Full Stack sample resume)
```
Predicted role: Full Stack Developer
Overall score: 100
ATS score: 100
Matched skills: [agile, bootstrap, css, express, git, html, javascript,
                 mongodb, node.js, python, react, rest api, sql]
Missing skills: [django, flask, graphql, next.js, redux, tailwind, typescript]
```

---

## 13. Results and Screenshots

*(For submission: capture and insert screenshots of the running application
at the following points — filenames are suggestions.)*

1. `screenshot_01_landing_hero.png` — Landing page hero section
2. `screenshot_02_register.png` — Registration form
3. `screenshot_03_login.png` — Login form
4. `screenshot_04_dashboard_empty.png` — Dashboard before any upload
5. `screenshot_05_upload_dragdrop.png` — Upload page with drag-and-drop zone
6. `screenshot_06_loading_overlay.png` — Loading animation during analysis
7. `screenshot_07_analysis_scores.png` — Analysis page: score gauges + chart
8. `screenshot_08_analysis_skills.png` — Matched/missing skill badges
9. `screenshot_09_analysis_ai_suggestions.png` — AI suggestions + interview questions panel
10. `screenshot_10_dashboard_populated.png` — Dashboard with resume history
11. `screenshot_11_pdf_report.png` — Downloaded PDF report opened in a viewer
12. `screenshot_12_dark_mode.png` — Any page in dark mode

---

## 14. Challenges Faced

1. **Inconsistent resume formatting** — resumes use wildly different
   layouts (tables, multi-column, mixed bullet styles). Solved by
   extracting text from both paragraphs *and* table cells in DOCX files,
   and normalizing whitespace before skill-matching.
2. **Balancing rule-based vs. AI-based scoring** — an early design used
   the LLM for scoring directly, but this produced non-reproducible scores
   across runs. The final design keeps scoring fully deterministic and uses
   the LLM only for free-text generation.
3. **Reliability without guaranteed internet/IBM access** — since grading
   environments may not have live IBM credentials, `ai_service.py` was
   built with a fully-functional, clearly-labeled local fallback for every
   AI-dependent feature.
4. **Keeping the UI professional, not generic** — a custom color system,
   typography pairing, and hand-built score-ring/progress components were
   used instead of default Bootstrap styling to avoid a templated look.

---

## 15. Future Scope

- Fine-tuning a Granite model on paired resume/job-description data for
  more precise role matching and truly personalized suggestions.
- A "paste a job description" mode for targeted gap analysis against a
  specific listing rather than a generic role.
- Resume version history with score-over-time trend charts.
- LinkedIn profile import via OAuth.
- Multi-language resume support (especially regional Indian languages).
- A recruiter-facing bulk-analysis mode for screening multiple candidates.
- Integration with IBM Watson Discovery for deeper structural document analysis.
- Migrating from SQLite to PostgreSQL for multi-user production deployment.

---

## 16. Conclusion

ResumeIQ demonstrates a complete, production-shaped full-stack application
that solves a real, relatable problem for students entering the job market.
It combines classical software-engineering rigor (a deterministic,
explainable scoring engine; a normalized relational schema; secure
authentication) with modern generative AI (IBM watsonx.ai's Granite model)
in a way that plays to each approach's strengths. The result is a tool that
is simultaneously reliable, explainable, and genuinely helpful — while also
serving as a strong demonstration of applying IBM's AI stack to a practical,
socially useful problem, in line with the goals of the IBM SkillsBuild
program.

---

## 17. References

1. IBM watsonx.ai Documentation — https://www.ibm.com/products/watsonx-ai
2. IBM Granite Foundation Models — https://www.ibm.com/granite
3. Flask Documentation — https://flask.palletsprojects.com
4. Flask-SQLAlchemy Documentation — https://flask-sqlalchemy.palletsprojects.com
5. Bootstrap 5 Documentation — https://getbootstrap.com
6. Chart.js Documentation — https://www.chartjs.org
7. ReportLab User Guide — https://www.reportlab.com/docs/reportlab-userguide.pdf
8. PyPDF2 Documentation — https://pypdf2.readthedocs.io
9. python-docx Documentation — https://python-docx.readthedocs.io

---

*End of Report*
