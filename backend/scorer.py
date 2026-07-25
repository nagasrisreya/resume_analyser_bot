def calculate_score(resume, jd):

    resume_skills = {
        s.lower()
        for s in resume["skills"]
    }

    required_skills = {
        s.lower()
        for s in jd["required_skills"]
    }

    matched = resume_skills & required_skills

    missing = required_skills - resume_skills

    if len(required_skills) == 0:
        skill_score = 0
    else:
        skill_score = (
            len(matched)
            /
            len(required_skills)
        ) * 70

    score = skill_score

    if resume["education"]:
        score += 10

    if len(resume["projects"]) > 0:
        score += 10

    if len(resume["certifications"]) > 0:
        score += 10

    return {
        "score": round(score, 2),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }