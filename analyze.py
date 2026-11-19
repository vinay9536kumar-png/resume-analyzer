import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from extract_resume import extract_text

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = MODEL = "gemini-3.5-flash-lite"

def analyze(resume_text, jd_text):
    prompt = f"""You are an expert technical recruiter. Compare the resume with the job description.

Return ONLY valid JSON in exactly this format:
{{
  "match_score": <integer 0-100>,
  "experience_level": "<Fresher | Junior | Mid-level | Senior>",
  "summary": "<2-3 sentence overall assessment>",
  "strengths": ["<point>", "<point>"],
  "missing_skills": ["<skill>", "<skill>"],
  "suggestions": ["<specific resume improvement>", "<specific resume improvement>"]
}}

Be honest and specific. Base everything only on the text given.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    return json.loads(response.text)

if __name__ == "__main__":
    resume_text = extract_text("resume.pdf")
    jd_text = open("jd.txt", encoding="utf-8").read()

    result = analyze(resume_text, jd_text)

    print("Match score:", result["match_score"], "%")
    print("Level:", result["experience_level"])
    print("\nSummary:", result["summary"])
    print("\nStrengths:")
    for s in result["strengths"]:
        print(" -", s)
    print("\nMissing skills:")
    for m in result["missing_skills"]:
        print(" -", m)
    print("\nSuggestions:")
    for s in result["suggestions"]:
        print(" -", s)
def rewrite_resume(resume_text, jd_text):
    prompt = f"""You are an expert resume writer. Rewrite the resume so it is tailored to the job description.

STRICT RULES:
- Use ONLY facts that are already in the resume. Never invent skills, projects, companies, degrees or numbers.
- Reword and reorder to highlight what is relevant to the job description.
- Use keywords from the job description only where the candidate genuinely has that experience.
- Use strong action verbs and short, clear bullet points.

Output in Markdown with these sections:
## Professional Summary (2-3 lines tailored to this job)
## Skills (most relevant to the job first)
## Projects (rewritten bullets, relevant ones first)
## Experience / Internships (rewritten bullets, if present)
## Education

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.4),
    )
    return response.text