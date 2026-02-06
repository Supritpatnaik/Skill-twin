import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load syllabus skills (from previous extraction)
with open('giet_cse_skills.json', 'r') as f:
    syllabus_data = json.load(f)
syllabus_skills = syllabus_data.get('overall_technical_skills', [])

embedder = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# 1. Extract skills from JD (paste or input)
# -----------------------------
def extract_skills(text, label="text"):
    prompt = f"""
    Extract all technical skills, tools, languages, frameworks from this {label}.
    Ignore soft skills unless explicitly technical.
    Output strict JSON only:
    {{"skills": ["Python", "AWS", "React", ...]}}
    Text: {text[:6000]}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)['skills']

# -----------------------------
# 2. Compute gaps
# -----------------------------
def compute_gaps(job_skills, student_plus_syllabus_skills):
    if not job_skills:
        return []

    job_emb = embedder.encode(job_skills)
    student_emb = embedder.encode(student_plus_syllabus_skills)

    gaps = []
    for i, skill in enumerate(job_skills):
        similarities = util.cos_sim(job_emb[i], student_emb)[0]
        best_match = similarities.max().item()
        if best_match < 0.55:
            gaps.append({
                "required_skill": skill,
                "best_match_score": round(best_match, 3),
                "gap_level": "High" if best_match < 0.40 else "Medium"
            })
    return sorted(gaps, key=lambda x: x['best_match_score'])

# -----------------------------
# 3. Generate bridge roadmap
# -----------------------------
def generate_roadmap(gaps, weeks=8):
    gaps_str = json.dumps(gaps, indent=2)
    prompt = f"""
    You are a career coach helping B.Tech CSE students in Odisha (Sambalpur/Bhubaneswar area).
    Student gaps from job: {gaps_str}

    Create a realistic {weeks}-week bridge learning plan.
    Prioritize **free resources** available in India/Odisha:
    - NPTEL / SWAYAM (free courses with certificate)
    - YouTube: Apna College, CodeWithHarry, Striver, Take U Forward
    - GeeksforGeeks, freeCodeCamp, W3Schools
    - Coursera/Google/IBM free audits

    Structure:
    - Start with highest gap skills
    - 10-15 hours/week
    - Each week: 1-2 main topics + 1 small project/task
    - Include links where possible (or course names)

    Output **strict JSON only**:
    {{
      "estimated_match_after": "75-85%",
      "total_weeks": {weeks},
      "roadmap": [
        {{
          "week": 1,
          "focus_skills": ["Docker basics", "Git advanced"],
          "resources": ["NPTEL Docker course", "YouTube: Apna College Git"],
          "project": "Set up a simple Docker container for a Python app",
          "hours": 12
        }},
        ...
      ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# -----------------------------
# MAIN FLOW - Run this
# -----------------------------
print("Skill-Twin Engine - Test Run")
print("=============================")

# Paste your real inputs here for testing
resume_text_or_path = "temp_resume.pdf"  # or paste text
jd_text = """
Job: Software Developer - Fresher
Skills required: Python, JavaScript, React, Node.js, SQL, Git, REST API, Problem Solving, AWS basics
Experience: 0-1 year, good communication
"""

# Step 1: Get student skills (from your parse_resume)
student_skills_dict = extract_resume_skills(resume_text_or_path)  # Reuse your function
student_skills = student_skills_dict.get('technical_skills', [])

# Step 2: Get job skills
job_skills = extract_skills(jd_text, "Job Description")

# Step 3: Combine student + syllabus
combined_known = list(set(student_skills + syllabus_skills))

# Step 4: Find gaps
gaps = compute_gaps(job_skills, combined_known)

print("\nJob Required Skills:", job_skills)
print("\nYour Known Skills (Resume + Syllabus):", combined_known[:20], "...")
print("\nDetected Gaps:")
for g in gaps:
    print(f"• {g['required_skill']} (match {g['best_match_score']}, {g['gap_level']})")

# Step 5: Generate roadmap
if gaps:
    roadmap = generate_roadmap(gaps, weeks=8)
    print("\nPersonalized Bridge Roadmap:")
    print(json.dumps(roadmap, indent=2))
else:
    print("\nNo significant gaps — you're well prepared!")