import re
from extract_resume import extract_text

SKILLS = [
    "python", "sql", "mysql", "git", "react", "machine learning",
    "deep learning", "nlp", "llm", "rag", "langchain", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch", "flask",
    "fastapi", "django", "api", "docker", "aws", "javascript",
]

def find_skills(text):
    text = text.lower()
    return {s for s in SKILLS if s in text}

resume_text = extract_text("resume.pdf")
jd_text = open("jd.txt", encoding="utf-8").read()

resume_skills = find_skills(resume_text)
jd_skills = find_skills(jd_text)

matched = resume_skills & jd_skills
missing = jd_skills - resume_skills
missing = jd_experience = [skill for skill in missing if skill in jd_text]
score = round(len(matched) / len(jd_skills) * 100) if jd_skills else 0

print("Match score:", score, "%")
print("Matched skills:", sorted(matched))
print("Missing skills:", sorted(missing))
print("Missing experience:", sorted(jd_experience))

def years_in_text(text):
    """Text में '2 years', '3+ years', '3-5 years' जैसे patterns से साल निकालता है।"""
    text = text.lower()
    years = []
    for lo, hi in re.findall(r"(\d+)\s*(?:-|to)\s*(\d+)\s*\+?\s*(?:years|yrs)", text):
        years.append(int(lo))  # range में न्यूनतम साल लेते हैं
    for y in re.findall(r"(\d+)\s*\+?\s*(?:years|yrs)", text):
        years.append(int(y))
    return years

def level_from_years(y):
    if y < 1:
        return "Fresher"
    if y < 3:
        return "Junior"
    if y < 6:
        return "Mid-level"
    return "Senior"

def resume_experience(text):
    t = text.lower()
    years = years_in_text(t)
    fresher_words = ["fresher", "intern", "internship", "student", "bca", "b.tech", "bsc", "graduate"]
    if years:
        return max(years)
    if any(w in t for w in fresher_words):
        return 0
    return 0

def jd_required_experience(text):
    years = years_in_text(text)
    return min(years) if years else 0

resume_years = resume_experience(resume_text)
jd_years = jd_required_experience(jd_text)

print("\nResume level:", level_from_years(resume_years), f"({resume_years} years)")
print("JD requires:", level_from_years(jd_years), f"({jd_years}+ years)")

if resume_years >= jd_years:
    print("Experience match: ✅")
else:
    print(f"Experience gap: JD को {jd_years} साल चाहिए, resume में {resume_years} साल दिखे ⚠️")