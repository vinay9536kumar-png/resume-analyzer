# 📄 AI Resume Analyzer

A Generative AI web app that compares your resume with a job description and gives you a match score, strengths, missing skills, and concrete suggestions to improve. It can also rewrite your resume to fit the job description.

## Features
- Upload a resume as a PDF and extract its text (PyMuPDF)
- Match score (0-100) against a job description
- Estimated experience level
- Strengths, missing skills, and resume improvement suggestions
- Rewrite your resume tailored to the job description (uses only facts already in your resume)
- Download the tailored resume as a text file
- Clean Streamlit interface

## Tech Stack
Python, Streamlit, PyMuPDF, Google Gemini API

## Project Structure
├── app.py # Streamlit UI
├── analyze.py # Gemini analysis and resume rewrite
├── extract_resume.py # PDF text extraction
├── requirements.txt
└── README.md

## Setup
1. Clone the repository:

git clone https://github.com/vinay9536kumar-png/resume-analyzer.git
cd resume-analyzer

2. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate

3. Install dependencies:

python -m pip install -r requirements.txt

4. Create a `.env` file in the project folder and add your Gemini API key:

GEMINI_API_KEY=your_key_here

5. Run the app:

streamlit run app.py


## How It Works
1. PyMuPDF extracts the text from the uploaded resume PDF.
2. The resume and job description are sent to Gemini in a structured prompt.
3. Gemini returns JSON with the score, strengths, gaps, and suggestions.
4. Streamlit displays the results. If requested, a second call produces a tailored version of the resume.

## Notes
- Never commit your `.env` file or API key.
- Scanned (image-only) PDFs are not supported, since they contain no extractable text.
- Always review the rewritten resume before using it.

## Author
Vinay Kumar