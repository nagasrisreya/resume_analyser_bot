import re


def extract_keywords(text):
    """
    Extract words from text.
    """
    words = re.findall(r"[A-Za-z][A-Za-z+#.]{1,}", text.lower())

    return set(words)


def calculate_score(resume_text, jd_text):

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = resume_keywords.intersection(jd_keywords)

    if len(jd_keywords) == 0:
        return 0, [], []

    score = round(
        len(matched) / len(jd_keywords) * 100,
        2
    )

    missing = sorted(jd_keywords - resume_keywords)

    return score, sorted(matched), missing