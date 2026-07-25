import unittest

from backend.extractor import normalize_resume_data


class NormalizeResumeDataTests(unittest.TestCase):
    def test_normalizes_resume_data_with_expected_schema(self):
        raw_resume = {
            "skills": ["Python", "Java"],
            "projects": ["CareerPath AI"],
            "education": "B.Tech AI & Data Science",
            "experience": ["AI/ML Intern"],
            "certifications": ["PyTorch"],
        }

        normalized = normalize_resume_data(raw_resume)

        self.assertEqual(normalized["candidate_name"], "")
        self.assertEqual(normalized["email"], "")
        self.assertEqual(normalized["phone"], "")
        self.assertEqual(normalized["cgpa"], "")
        self.assertEqual(normalized["university"], "")
        self.assertEqual(normalized["degree"], "")
        self.assertEqual(normalized["graduation_year"], "")
        self.assertEqual(normalized["skills"], ["Python", "Java"])
        self.assertEqual(normalized["projects"], ["CareerPath AI"])
        self.assertEqual(normalized["experience"], ["AI/ML Intern"])
        self.assertEqual(normalized["certifications"], ["PyTorch"])


if __name__ == "__main__":
    unittest.main()
