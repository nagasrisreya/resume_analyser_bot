from backend.groq_client import call_groq
from backend.json_parser import extract_json


def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    if isinstance(value, str):
        return [value] if value.strip() else []
    return [str(value)]


def normalize_resume_data(raw_resume):
    if not isinstance(raw_resume, dict):
        raw_resume = {}

    degree_value = raw_resume.get("degree") or ""
    education_value = raw_resume.get("education") or ""
    university_value = raw_resume.get("university") or ""

    return {
        "candidate_name": str(raw_resume.get("candidate_name") or raw_resume.get("name") or ""),
        "email": str(raw_resume.get("email") or ""),
        "phone": str(raw_resume.get("phone") or ""),
        "cgpa": str(raw_resume.get("cgpa") or ""),
        "university": str(university_value or ""),
        "degree": str(degree_value or ""),
        "graduation_year": str(raw_resume.get("graduation_year") or ""),
        "skills": _ensure_list(raw_resume.get("skills")),
        "projects": _ensure_list(raw_resume.get("projects")),
        "experience": _ensure_list(raw_resume.get("experience")),
        "certifications": _ensure_list(raw_resume.get("certifications")),
        "education": str(education_value or ""),
    }


def extract_resume_info(text):

    prompt = f"""
You are an ATS parser.

Extract ONLY the following information from this resume.

Return ONLY valid JSON.

{{
  "candidate_name":"",
  "email":"",
  "phone":"",
  "cgpa":"",
  "university":"",
  "degree":"",
  "graduation_year":"",
  "skills":[],
  "projects":[],
  "experience":[],
  "certifications":[]
}}

Resume:

{text}
"""

    result = call_groq(prompt)

    try:
        parsed = extract_json(result)
    except Exception:
        parsed = {}

    return normalize_resume_data(parsed)


def extract_jd_info(text):

    prompt = f"""
You are an ATS parser.

Extract ONLY the following.

Return ONLY JSON.

{{
"required_skills":[],
"preferred_skills":[],
"education_required":"",
"experience_required":"",
"job_title":"",
"company":""
}}

Job Description

{text}
"""

    result = call_groq(prompt)

    try:
        parsed = extract_json(result)
    except Exception:
        parsed = {}

    if not isinstance(parsed, dict):
        parsed = {}

    return {
        "required_skills": _ensure_list(parsed.get("required_skills")),
        "preferred_skills": _ensure_list(parsed.get("preferred_skills")),
        "education_required": str(parsed.get("education_required") or ""),
        "experience_required": str(parsed.get("experience_required") or ""),
        "job_title": str(parsed.get("job_title") or ""),
        "company": str(parsed.get("company") or ""),
    }