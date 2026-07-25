from backend.groq_client import call_groq


def ask_resume_question(question, analysis):
    """
    Answer questions about ATS analysis results using Groq.

    Args:
        question: The user's question
        analysis: dict with keys "jd" (list of dicts) and "resumes" (list of dicts)
    """
    jds = analysis.get("jd", [])
    resumes = analysis.get("resumes", [])

    # Build JD summary (now supports multiple JDs)
    jd_summary_parts = ["Job Descriptions Analysed:\n"]
    for i, j in enumerate(jds, start=1):
        jd = j.get("data", {})
        jd_summary_parts.append(f"""
JD {i}: {j.get('name', 'Unknown')}
  - Job Title: {jd.get('job_title', 'N/A')}
  - Company: {jd.get('company', 'N/A')}
  - Required Skills: {', '.join(jd.get('required_skills', [])) or 'None'}
  - Preferred Skills: {', '.join(jd.get('preferred_skills', [])) or 'None'}
  - Education Required: {jd.get('education_required', 'N/A')}
  - Experience Required: {jd.get('experience_required', 'N/A')}
""")
    jd_summary = "\n".join(jd_summary_parts)

    resumes_summary = "Resumes Analysed:\n"
    for i, r in enumerate(resumes, start=1):
        resume = r.get("data", {}) or r.get("resume_json", {})
        resumes_summary += f"""
Resume {i}: {r.get('name', 'Unknown')}
  - Candidate Name: {resume.get('candidate_name') or 'N/A'}
  - Email: {resume.get('email') or 'N/A'}
  - Phone: {resume.get('phone') or 'N/A'}
  - CGPA: {resume.get('cgpa') or 'N/A'}
  - University: {resume.get('university') or 'N/A'}
  - Degree: {resume.get('degree') or 'N/A'}
  - Graduation Year: {resume.get('graduation_year') or 'N/A'}
  - Skills: {', '.join(resume.get('skills', [])) or 'None'}
  - Projects: {', '.join(resume.get('projects', [])) or 'None'}
  - Experience: {', '.join(resume.get('experience', [])) or 'None'}
  - Certifications: {', '.join(resume.get('certifications', [])) or 'None'}
  - ATS Score: {r.get('score', 'N/A')}%
  - Matched Skills: {', '.join(r.get('matched', [])) or 'None'}
  - Missing Skills: {', '.join(r.get('missing', [])) or 'None'}
"""

    prompt = f"""
You are an ATS Career Assistant.

Below is the ATS analysis data.

{jd_summary}

{resumes_summary}

Answer ONLY using the information provided above.

If the user asks about:
• courses
• projects
• missing skills
• ATS score
• resume improvements

give professional, actionable suggestions.

User Question:
{question}
"""

    return call_groq(prompt)
