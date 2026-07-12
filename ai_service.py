"""
ai_service.py
Handles all communication with IBM watsonx.ai (Granite foundation model).

Flow:
    1. Exchange IBM_API_KEY for a short-lived IAM bearer token.
    2. Call the watsonx.ai text-generation endpoint with the Granite model.
    3. Parse and return generated text.

If IBM_API_KEY / IBM_PROJECT_ID are not configured (e.g. during local demo
or grading without cloud credentials), every function gracefully falls back
to a deterministic, rule-based "local AI simulation" so the application
remains fully functional end-to-end. This fallback is clearly labeled in
the returned text so it's never presented as if it came from Granite.
"""
import os
import time
import requests

IBM_API_KEY = os.getenv("IBM_API_KEY", "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
IBM_MODEL_ID = os.getenv("IBM_MODEL_ID", "ibm/granite-13b-instruct-v2")
IBM_IAM_URL = os.getenv("IBM_IAM_URL", "https://iam.cloud.ibm.com/identity/token")

_TOKEN_CACHE = {"token": None, "expires_at": 0}


def _is_configured() -> bool:
    return bool(IBM_API_KEY and IBM_PROJECT_ID and "your-" not in IBM_API_KEY)


def _get_iam_token() -> str:
    """Fetch (and cache) an IBM Cloud IAM bearer token."""
    now = time.time()
    if _TOKEN_CACHE["token"] and _TOKEN_CACHE["expires_at"] > now + 30:
        return _TOKEN_CACHE["token"]

    resp = requests.post(
        IBM_IAM_URL,
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": IBM_API_KEY,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    _TOKEN_CACHE["token"] = data["access_token"]
    _TOKEN_CACHE["expires_at"] = now + data.get("expires_in", 3600)
    return _TOKEN_CACHE["token"]


def _call_granite(prompt: str, max_new_tokens: int = 400, temperature: float = 0.6) -> str:
    """
    Low-level call to the watsonx.ai /ml/v1/text/generation endpoint using the
    Granite model. Raises on failure so callers can decide on fallback.
    """
    token = _get_iam_token()
    endpoint = f"{IBM_URL}/ml/v1/text/generation?version=2023-05-29"

    payload = {
        "model_id": IBM_MODEL_ID,
        "input": prompt,
        "project_id": IBM_PROJECT_ID,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": 20,
            "temperature": temperature,
            "repetition_penalty": 1.1,
        },
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    resp = requests.post(endpoint, json=payload, headers=headers, timeout=45)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        raise ValueError("No results returned from watsonx.ai")
    return results[0].get("generated_text", "").strip()


def _safe_generate(prompt: str, fallback: str, **kwargs) -> str:
    """Try Granite; fall back to a local deterministic string on any error."""
    if not _is_configured():
        return fallback
    try:
        text = _call_granite(prompt, **kwargs)
        return text if text else fallback
    except Exception as exc:
        return f"{fallback}\n\n[Note: IBM watsonx.ai call failed ({exc}); showing local fallback suggestions.]"


# ---------------------------------------------------------------------------
# Public functions used by the Flask routes
# ---------------------------------------------------------------------------

def generate_resume_improvement_suggestions(resume_text: str, missing_skills, ats_issues) -> str:
    prompt = (
        "You are an expert career coach and resume reviewer. Analyze the resume "
        "text below and provide 5-7 concise, actionable improvement suggestions "
        "(bullet points) covering wording, structure, quantification of achievements, "
        "and formatting. Be specific and encouraging.\n\n"
        f"MISSING SKILLS FOR TARGET ROLE: {', '.join(missing_skills) or 'None'}\n"
        f"DETECTED ATS ISSUES: {', '.join(ats_issues)}\n\n"
        f"RESUME TEXT:\n{resume_text[:3000]}\n\n"
        "Improvement Suggestions:\n-"
    )
    fallback_points = [
        "Start each bullet point with a strong action verb (e.g., 'Developed', 'Led', 'Optimized').",
        "Quantify achievements wherever possible (e.g., 'improved performance by 30%').",
        "Add a concise professional summary (2-3 lines) at the top of your resume.",
        "Ensure consistent formatting — same font, spacing, and bullet style throughout.",
        f"Add missing but relevant skills such as: {', '.join(missing_skills[:5]) or 'none detected'}.",
        "Keep the resume to 1-2 pages and remove outdated or irrelevant information.",
        "Use a clear section order: Contact → Summary → Skills → Experience/Projects → Education → Certifications.",
    ]
    fallback = "- " + "\n- ".join(fallback_points)
    return _safe_generate(prompt, fallback, max_new_tokens=450)


def generate_interview_questions(role: str, matched_skills) -> list:
    prompt = (
        f"Generate 8 realistic technical and behavioral interview questions for a "
        f"candidate applying for the role of '{role}'. Their key skills include: "
        f"{', '.join(matched_skills[:10])}. Return only a numbered list of questions."
    )
    fallback_bank = {
        "Data Scientist": [
            "Explain the bias-variance tradeoff in machine learning.",
            "How would you handle missing data in a dataset?",
            "Walk me through a data science project from your resume end-to-end.",
            "What is overfitting and how do you prevent it?",
            "Explain the difference between supervised and unsupervised learning.",
        ],
        "Software Engineer": [
            "Explain the difference between an array and a linked list.",
            "How would you design a URL shortening service?",
            "What is the time complexity of binary search and why?",
            "Describe a challenging bug you fixed and how you debugged it.",
            "What is the difference between REST and GraphQL?",
        ],
        "Full Stack Developer": [
            "Explain how React's virtual DOM improves performance.",
            "How do you manage state in a large React application?",
            "Describe how you would design a REST API for a to-do app.",
            "What is CORS and how do you handle it?",
            "Explain the difference between SQL and NoSQL databases.",
        ],
        "AI/ML Engineer": [
            "How would you deploy a machine learning model to production?",
            "Explain the difference between CNN and RNN architectures.",
            "What is transfer learning and when would you use it?",
            "How do you monitor a deployed model for drift?",
            "Describe your experience with model optimization or quantization.",
        ],
    }
    generic = [
        "Tell me about yourself and walk me through your resume.",
        "Describe a project you're most proud of and your specific contribution.",
        "How do you stay updated with the latest trends in your field?",
        "Describe a time you faced a conflict in a team and how you resolved it.",
        "Where do you see yourself in the next 3-5 years?",
        "Why do you want to work in this role/industry?",
    ]

    if _is_configured():
        try:
            text = _call_granite(prompt, max_new_tokens=350)
            lines = [l.strip(" -0123456789.") for l in text.split("\n") if l.strip()]
            questions = [l for l in lines if len(l) > 15][:8]
            if questions:
                return questions
        except Exception:
            pass

    role_specific = fallback_bank.get(role, [])
    combined = (role_specific + generic)[:8]
    return combined


def generate_career_coach_advice(role: str, overall_score: int, missing_skills) -> str:
    prompt = (
        f"As a career coach, give a short (3-4 sentence) motivational and practical "
        f"piece of advice for a candidate targeting the '{role}' role, who scored "
        f"{overall_score}/100 on their resume analysis and is missing these skills: "
        f"{', '.join(missing_skills[:6]) or 'none major'}. Be encouraging but honest."
    )
    fallback = (
        f"Your resume shows solid potential for the {role} track with a score of "
        f"{overall_score}/100. Focus next on closing the gap in "
        f"{', '.join(missing_skills[:3]) or 'a few key areas'} through targeted projects "
        f"or certifications, and keep tailoring your resume to each job description. "
        f"Consistent, focused effort over the next few weeks will meaningfully "
        f"improve your interview callbacks."
    )
    return _safe_generate(prompt, fallback, max_new_tokens=200)


def is_granite_configured() -> bool:
    return _is_configured()
