import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import pdfplumber  # Reuse for PDF resumes

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_resume_skills(pdf_path_or_text):
    if os.path.exists(pdf_path_or_text):  # PDF file
        with pdfplumber.open(pdf_path_or_text) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    else:
        text = pdf_path_or_text  # raw text input

    prompt = f"""
    Extract all technical and soft skills from this student resume text.
    Include programming languages, tools, frameworks, projects, certifications.
    Output strict JSON: {{
      "technical_skills": ["Python", "SQL", ...],
      "soft_skills": ["Teamwork", ...],
      "projects": ["Built ML model using Python", ...]
    }}
    Text: {text[:5000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Test with sample
sample_resume = """
Skills: Python, Java, SQL, Machine Learning, Git
Projects: E-commerce website using React & Node.js
"""
skills = extract_resume_skills(sample_resume)
with open('sample_student_skills.json', 'w') as f:
    json.dump(skills, f, indent=2)

print("Student skills saved!")