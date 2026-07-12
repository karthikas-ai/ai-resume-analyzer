"""
analyzer.py
Rule-based resume analysis engine: scoring, skill detection, ATS
compatibility checks, and career-role prediction. This is deterministic
(no external API needed) so the app is fully functional even without
IBM credentials. IBM Granite is layered on top for natural-language
suggestions, interview questions, and improvement advice (see ai_service.py).
"""
import re

# ---------------------------------------------------------------------------
# Skill taxonomy: role -> set of relevant skills/keywords (lowercase)
# ---------------------------------------------------------------------------
ROLE_SKILLS = {
    "Data Scientist": {
        "python", "r", "sql", "machine learning", "deep learning", "pandas",
        "numpy", "scikit-learn", "tensorflow", "pytorch", "data visualization",
        "statistics", "nlp", "computer vision", "tableau", "power bi",
        "matplotlib", "seaborn", "keras", "hadoop", "spark",
    },
    "Software Engineer": {
        "java", "python", "c++", "c", "data structures", "algorithms",
        "git", "rest api", "sql", "oop", "system design", "docker",
        "kubernetes", "microservices", "unit testing", "agile", "linux",
    },
    "Full Stack Developer": {
        "javascript", "react", "node.js", "html", "css", "mongodb",
        "express", "rest api", "typescript", "redux", "next.js", "sql",
        "git", "bootstrap", "tailwind", "graphql", "flask", "django",
    },
    "AI/ML Engineer": {
        "python", "machine learning", "deep learning", "tensorflow",
        "pytorch", "keras", "nlp", "computer vision", "opencv",
        "scikit-learn", "mlops", "docker", "flask", "fastapi", "pandas",
        "numpy", "data preprocessing", "model deployment",
    },
    "Business Analyst": {
        "sql", "excel", "power bi", "tableau", "data analysis",
        "requirements gathering", "stakeholder management", "jira",
        "agile", "business intelligence", "financial modeling",
    },
    "Cloud Engineer": {
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "ci/cd", "jenkins", "linux", "networking", "cloud security",
        "devops", "ansible",
    },
    "Cybersecurity Analyst": {
        "network security", "penetration testing", "siem", "firewall",
        "vulnerability assessment", "incident response", "cryptography",
        "linux", "python", "risk assessment", "compliance",
    },
    "UI/UX Designer": {
        "figma", "adobe xd", "sketch", "wireframing", "prototyping",
        "user research", "usability testing", "design systems",
        "photoshop", "illustrator", "interaction design",
    },
}

# Flatten set of all known skills across roles for general skill detection
ALL_SKILLS = sorted({s for skills in ROLE_SKILLS.values() for s in skills})

SECTION_KEYWORDS = {
    "contact": ["email", "phone", "linkedin", "@"],
    "summary": ["summary", "objective", "profile"],
    "education": ["education", "degree", "university", "college", "b.e", "b.tech", "bachelor", "master"],
    "experience": ["experience", "internship", "work history", "employment"],
    "skills": ["skills", "technical skills", "competencies"],
    "projects": ["project", "projects"],
    "certifications": ["certification", "certificate", "certified"],
}

ATS_RED_FLAGS = [
    (r"\.(png|jpg|jpeg)", "Avoid embedding photos/images — many ATS systems cannot parse them."),
    (r"\btable\b", None),  # handled separately via docx tables, placeholder
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def detect_skills(resume_text: str):
    """Return list of known skills found anywhere in the resume text."""
    text = _normalize(resume_text)
    found = []
    for skill in ALL_SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(set(found))


def predict_role(matched_skills):
    """Predict the best-fit career role based on skill overlap."""
    if not matched_skills:
        return "General / Entry-Level Candidate", {}

    matched_set = set(matched_skills)
    scores = {}
    for role, role_skills in ROLE_SKILLS.items():
        overlap = matched_set & role_skills
        if role_skills:
            scores[role] = round(len(overlap) / len(role_skills) * 100, 1)

    best_role = max(scores, key=scores.get)
    return best_role, scores


def missing_skills_for_role(matched_skills, role):
    role_skills = ROLE_SKILLS.get(role, set())
    missing = sorted(role_skills - set(matched_skills))
    return missing


def check_sections_present(resume_text: str):
    text = _normalize(resume_text)
    present = {}
    for section, keywords in SECTION_KEYWORDS.items():
        present[section] = any(kw in text for kw in keywords)
    return present


def ats_compatibility_check(resume_text: str, filename: str):
    """
    Rule-based ATS (Applicant Tracking System) compatibility scoring.
    Checks structure, length, formatting cues, and section completeness.
    """
    issues = []
    score = 100
    text = resume_text
    word_count = len(text.split())

    sections = check_sections_present(text)

    if not sections["contact"]:
        issues.append("No clear contact information (email/phone) detected.")
        score -= 15
    if not sections["skills"]:
        issues.append("No dedicated 'Skills' section detected.")
        score -= 15
    if not sections["education"]:
        issues.append("No 'Education' section detected.")
        score -= 10
    if not sections["experience"] and not sections["projects"]:
        issues.append("No 'Experience' or 'Projects' section detected.")
        score -= 15

    if word_count < 150:
        issues.append("Resume seems too short (under 150 words) — add more detail.")
        score -= 15
    elif word_count > 1200:
        issues.append("Resume is very long — consider trimming to 1-2 pages.")
        score -= 5

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        issues.append("Resume submitted as an image — ATS cannot parse images.")
        score -= 30

    bullet_markers = len(re.findall(r"[•\-\*]\s", text))
    if bullet_markers < 3:
        issues.append("Few or no bullet points detected — use bullets for readability by ATS parsers.")
        score -= 5

    if re.search(r"\btable\b", text.lower()) and False:
        # placeholder for future table-detection heuristics
        pass

    score = max(0, min(100, score))
    if not issues:
        issues.append("No major ATS issues detected. Resume structure looks solid.")

    return score, issues


def calculate_overall_score(matched_skills, ats_score, sections, word_count):
    """
    Composite score (0-100) combining:
      - Skill coverage (40%)
      - ATS compatibility (35%)
      - Section completeness (15%)
      - Length appropriateness (10%)
    """
    skill_component = min(len(matched_skills) / 12, 1.0) * 40
    ats_component = (ats_score / 100) * 35
    section_component = (sum(sections.values()) / len(sections)) * 15
    length_component = 10 if 150 <= word_count <= 1200 else 5

    total = skill_component + ats_component + section_component + length_component
    return round(min(100, max(0, total)))


def learning_recommendations(missing_skills, role):
    """Suggest learning resources for the top missing skills."""
    recs = []
    course_map = {
        "python": "Python for Everybody (Coursera) / IBM Python for Data Science",
        "machine learning": "Machine Learning by Andrew Ng (Coursera)",
        "deep learning": "Deep Learning Specialization (Coursera)",
        "sql": "SQL for Data Science (Coursera) / Mode SQL Tutorial",
        "docker": "Docker & Kubernetes: The Practical Guide (Udemy)",
        "aws": "AWS Cloud Practitioner Essentials (AWS Skill Builder)",
        "react": "React - The Complete Guide (Udemy)",
        "tensorflow": "TensorFlow Developer Certificate (Coursera)",
        "power bi": "Microsoft Power BI Desktop for Business Intelligence (Udemy)",
        "figma": "Figma UI/UX Design Essentials (Udemy)",
    }
    for skill in missing_skills[:8]:
        resource = course_map.get(skill, f"Search '{skill.title()}' on IBM SkillsBuild / Coursera")
        recs.append({"skill": skill.title(), "resource": resource})
    return recs


def full_local_analysis(resume_text: str, filename: str):
    """Runs the entire deterministic pipeline and returns a result dict."""
    matched_skills = detect_skills(resume_text)
    predicted_role, role_scores = predict_role(matched_skills)
    missing = missing_skills_for_role(matched_skills, predicted_role)
    sections = check_sections_present(resume_text)
    ats_score, ats_issues = ats_compatibility_check(resume_text, filename)
    word_count = len(resume_text.split())
    overall_score = calculate_overall_score(matched_skills, ats_score, sections, word_count)
    recs = learning_recommendations(missing, predicted_role)

    return {
        "matched_skills": matched_skills,
        "predicted_role": predicted_role,
        "role_scores": role_scores,
        "missing_skills": missing,
        "sections": sections,
        "ats_score": ats_score,
        "ats_issues": ats_issues,
        "overall_score": overall_score,
        "learning_recommendations": recs,
        "word_count": word_count,
    }
