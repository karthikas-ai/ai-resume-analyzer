# Presentation Content — 12 Slides
## AI Resume Analyzer & Career Coach (ResumeIQ)
*IBM SkillsBuild / Edunet Foundation Final Project*

> Use this as the script/content source if generating an actual .pptx file
> (e.g., via the pptx skill, PowerPoint, or Canva). Each slide lists a
> suggested title, bullet content, and a visual note.

---

### Slide 1 — Title Slide
**Title:** AI Resume Analyzer & Career Coach
**Subtitle:** Turning resume feedback into a data-driven, AI-powered experience
**Footer:** IBM SkillsBuild × Edunet Foundation | [Your Name] | [Date]
**Visual:** App logo/wordmark ("ResumeIQ"), soft indigo gradient background

---

### Slide 2 — Problem Statement
**Title:** The Problem
- 75%+ of resumes are filtered by ATS software before a human ever sees them
- Students rarely get fast, objective, specific feedback on their resumes
- Generic advice ("add more skills") isn't actionable
- Career-role fit is unclear without a target job description to compare against

**Visual:** Funnel graphic — resumes submitted → ATS filtered → human-reviewed

---

### Slide 3 — Objective
**Title:** Project Objective
- Build a full-stack web app that scores resumes (0–100) automatically
- Detect ATS compatibility issues before submission
- Predict the candidate's best-fit career role from their skills
- Use IBM watsonx.ai (Granite) to generate personalized, natural-language coaching
- Provide a downloadable, shareable PDF report

**Visual:** Simple icon row: Upload → Analyze → Improve → Apply

---

### Slide 4 — Tech Stack
**Title:** Technology Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js
- **AI:** IBM watsonx.ai — Granite Foundation Model
- **Database:** SQLite
- **Parsing/Reporting:** PyPDF2, python-docx, ReportLab

**Visual:** Logo grid of the technologies

---

### Slide 5 — System Architecture
**Title:** System Architecture
- Browser (Bootstrap UI) ↔ Flask App ↔ SQLite Database
- Service layer: resume_parser → analyzer → ai_service → report_generator
- IBM watsonx.ai called via IAM-authenticated REST API
- Hybrid design: deterministic scoring + generative AI coaching

**Visual:** The architecture diagram from README.md / PROJECT_REPORT.md

---

### Slide 6 — Core Feature: Resume Scoring Engine
**Title:** How the Score Is Calculated
- Skill Coverage — 40%
- ATS Compatibility — 35%
- Section Completeness — 15%
- Length Appropriateness — 10%
- Fully transparent and reproducible — no black box

**Visual:** Donut chart showing the 4 weighted components

---

### Slide 7 — Core Feature: ATS Compatibility Check
**Title:** ATS Compatibility Check
- Detects missing contact info, skills, education, experience sections
- Flags overly short/long resumes
- Flags image-only (non-parseable) resumes
- Checks bullet-point usage for structure

**Visual:** Before/after mock resume with red flags annotated

---

### Slide 8 — Core Feature: Career Role Prediction
**Title:** Career Role Prediction & Skill Gap Analysis
- 8 career tracks: Data Scientist, Software Engineer, Full Stack Developer,
  AI/ML Engineer, Business Analyst, Cloud Engineer, Cybersecurity Analyst, UI/UX Designer
- Matches detected skills against each role's skill profile
- Surfaces the specific missing skills for the best-fit role
- Maps each missing skill to a learning resource

**Visual:** Screenshot of matched/missing skill badges from the app

---

### Slide 9 — IBM watsonx.ai Integration
**Title:** Powered by IBM Granite
- IAM token exchange → authenticated calls to watsonx.ai text-generation API
- 3 use cases: improvement suggestions, interview questions, career coach advice
- Prompt engineering grounded in the candidate's actual resume + analysis data
- Automatic, clearly-labeled local fallback if credentials aren't configured — the app always works

**Visual:** IBM watsonx.ai logo + simplified request/response flow diagram

---

### Slide 10 — UI/UX Highlights
**Title:** Designed for Real Students
- Clean, professional indigo/teal design system
- Dark/light mode toggle
- Drag-and-drop upload with loading animation
- Interactive charts and circular score gauges
- Fully responsive across desktop and mobile

**Visual:** Side-by-side screenshots — light mode & dark mode

---

### Slide 11 — Demo / Results
**Title:** Sample Results
- Sample resume → Predicted Role: Full Stack Developer, Score: 100/100
- Sample resume → Predicted Role: Data Scientist, Score: 97/100
- Full analysis pipeline runs in under 5 seconds (excluding live AI latency)
- One-click PDF report export

**Visual:** Screenshot of the analysis results page + the exported PDF

---

### Slide 12 — Conclusion & Future Scope
**Title:** Conclusion & What's Next
- Delivered a complete, working, IBM-Granite-powered resume analysis platform
- Combines explainable rule-based scoring with generative AI coaching
- **Future scope:** job-description-specific matching, fine-tuned Granite
  model, LinkedIn import, score-over-time tracking, multi-language support

**Visual:** Thank-you slide with contact info / GitHub repo link

---

*End of presentation content.*
