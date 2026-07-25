import os

from backend.parser import parse_document
from backend.extractor import extract_resume_info, extract_jd_info
from backend.scorer import calculate_score

resume_folder = "uploads/resumes"
jd_folder = "uploads/jd"

resume_files = os.listdir(resume_folder)
jd_files = os.listdir(jd_folder)

print("Resume Files:", resume_files)
print("JD Files:", jd_files)

resume_path = os.path.join(resume_folder, resume_files[0])
jd_path = os.path.join(jd_folder, jd_files[0])

print("Using Resume:", resume_path)
print("Using JD:", jd_path)

resume_text = parse_document(resume_path)
jd_text = parse_document(jd_path)

resume_json = extract_resume_info(resume_text)
jd_json = extract_jd_info(jd_text)

result = calculate_score(resume_json, jd_json)

print(result)