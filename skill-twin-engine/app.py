# app.py - Updated Skill-Twin Engine (with tree roadmap, deadline adjustment)

import streamlit as st
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import pdfplumber
from datetime import datetime, timedelta

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────

def extract_skills(text, label="text"):
    prompt = f"""
    Extract all technical skills, programming languages, tools, frameworks from this {label}.
    Only return technical/professional skills. Ignore soft skills unless they are technical.
    Output strict JSON only:
    {{"technical_skills": ["Python", "SQL", ...]}}
    Text: {text[:5000]}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)["technical_skills"]
    except Exception as e:
        st.error(f"Skill extraction error: {e}")
        return []

def validate_skills(extracted_skills):
    # Common technical skills database for validation
    trusted_skills_db = set([
        # Programming Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "Go", "Rust", "Swift", "Kotlin", "PHP",
        # Frameworks & Libraries
        "React", "Angular", "Vue.js", "Svelte", "Django", "Flask", "FastAPI", "Spring", "Node.js", 
        "Express", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Bootstrap", "jQuery",
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab CI", "Terraform",
        # Tools & Technologies
        "Git", "Linux", "Bash", "REST API", "GraphQL", "API", "CI/CD", "Agile", "Scrum",
        # Specialized Skills
        "Machine Learning", "Deep Learning", "Data Science", "AI", "NLP", "Computer Vision",
        "Cybersecurity", "DevOps", "Microservices", "Testing", "JUnit", "Selenium"
    ])
    
    validated_skills = []
    uncertain_skills = []
    
    for skill in extracted_skills:
        # Normalize skill for comparison
        normalized_skill = skill.strip().lower()
        if normalized_skill in [s.lower() for s in trusted_skills_db]:
            validated_skills.append(skill)
        else:
            # Check if it's a common variation or similar to trusted skills
            is_valid = False
            for trusted_skill in trusted_skills_db:
                if normalized_skill.replace(" ", "") == trusted_skill.replace(" ", "").lower():
                    validated_skills.append(skill)
                    is_valid = True
                    break
            if not is_valid:
                uncertain_skills.append(skill)
    
    return validated_skills, uncertain_skills


def extraction_quality_report(original_text, extracted_skills):
    # Calculate text coverage
    if not original_text or len(original_text) == 0:
        return {
            "quality_score": 0,
            "total_skills_extracted": len(extracted_skills),
            "estimated_accuracy": "Low"
        }
    
    # Calculate ratio of skills to text length
    text_length = len(original_text)
    skills_text_length = sum(len(skill) for skill in extracted_skills)
    coverage_ratio = skills_text_length / text_length if text_length > 0 else 0
    
    # Calculate quality score (0-100)
    quality_score = min(coverage_ratio * 500, 100)  # Adjust multiplier based on expected ratios
    
    # Estimate accuracy based on coverage and number of skills
    if quality_score > 50 and len(extracted_skills) >= 3:
        estimated_accuracy = "High"
    elif quality_score > 20 and len(extracted_skills) >= 1:
        estimated_accuracy = "Medium"
    else:
        estimated_accuracy = "Low"
    
    return {
        "quality_score": round(quality_score, 2),
        "total_skills_extracted": len(extracted_skills),
        "estimated_accuracy": estimated_accuracy
    }

def extract_from_pdf(uploaded_file, label="document"):
    if uploaded_file is None:
        return []
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages if page.extract_text())
        extracted_skills = extract_skills(text, label)
        
        # Validate extracted skills
        validated, uncertain = validate_skills(extracted_skills)
        if uncertain:
            st.warning(f"Found {len(uncertain)} skills that need manual verification: {', '.join(uncertain[:3])}{'...' if len(uncertain) > 3 else ''}")
        
        # Show extraction quality report
        quality_report = extraction_quality_report(text, extracted_skills)
        st.info(f"Extraction quality: {quality_report['estimated_accuracy']} ({quality_report['quality_score']:.1f}%) - {quality_report['total_skills_extracted']} skills extracted")
        
        return validated  # Return only validated skills
    except Exception as e:
        st.error(f"Could not read {label} PDF: {e}")
        return []

def generate_typical_job_skills(role_name):
    prompt = f"""
    You are a placement expert for engineering freshers in India (2026 market).
    For the job role: "{role_name}" (fresher level, 0-1 year experience)

    List 8-15 most common technical skills required.
    Only technical skills/tools/languages/frameworks.
    Output strict JSON:
    {{"skills": ["Python", "SQL", "React", ...]}}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        return json.loads(response.choices[0].message.content)["skills"]
    except:
        return []

def compute_gaps(job_skills, known_skills):
    if not job_skills or not known_skills:
        return []
    job_emb = embedder.encode(job_skills)
    known_emb = embedder.encode(known_skills)
    gaps = []
    for i, skill in enumerate(job_skills):
        sims = util.cos_sim(job_emb[i], known_emb)[0]
        best = sims.max().item()
        if best < 0.55:
            gaps.append({
                "skill": skill,
                "match": round(best, 2),
                "level": "High" if best < 0.4 else "Medium"
            })
    return sorted(gaps, key=lambda x: x["match"])

def generate_roadmap(gaps, weeks=8):
    gaps_str = json.dumps(gaps, indent=2)
    prompt = f"""
    You are a career coach for B.Tech students in Odisha.
    Gaps from job role: {gaps_str}

    Create a realistic {weeks}-week bridge plan.
    Divide the plan into a tree structure: each week focuses on 1-2 major skills, with sub-recommendations for each skill (resources, practice, project).
    Use free resources: NPTEL, SWAYAM, YouTube (Apna College, CodeWithHarry, Striver), GeeksforGeeks, freeCodeCamp.

    Output strict JSON:
    {{
      "estimated_match_after": "75-85%",
      "total_weeks": {weeks},
      "roadmap": [
        {{
          "week": 1,
          "focus_skills": [["Docker basics", "Recommendations: Learn containerization with NPTEL course, Practice on local machine, Project: Deploy simple app"]],
          "hours": 12
        }},
        ...
      ]
    }}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except:
        return {}

# ────────────────────────────────────────────────
# Streamlit UI
# ────────────────────────────────────────────────

st.title("Skill-Twin Engine")
st.markdown("Upload your resume and/or syllabus → choose job role → get gaps & customized plan")

# 1. User basic info
st.subheader("Your Details")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name")
with col2:
    branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "ME", "CE", "Other"])

year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th"])
if st.button("Save Info"):
    st.session_state.user = {"name": name, "branch": branch, "year": year}
    st.success("Info saved!")

# 2. Mandatory: at least one of resume or syllabus
st.subheader("Upload Documents (at least one required)")
col_resume, col_syllabus = st.columns(2)

with col_resume:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")

with col_syllabus:
    syllabus_file = st.file_uploader("Upload Syllabus (PDF)", type=["pdf"], key="syllabus")

# Extract skills
resume_skills = []
syllabus_skills = []

if resume_file:
    resume_skills = extract_from_pdf(resume_file, "resume")
    if resume_skills:
        st.success(f"Validated {len(resume_skills)} skills from resume")

if syllabus_file:
    syllabus_skills = extract_from_pdf(syllabus_file, "syllabus")
    if syllabus_skills:
        st.success(f"Validated {len(syllabus_skills)} skills from syllabus")

# If one is missing → ask user manually
known_skills = list(set(resume_skills + syllabus_skills))

if not known_skills:
    st.error("You must upload at least one document (resume or syllabus)")
    st.stop()

missing_resume = not resume_file or not resume_skills
missing_syllabus = not syllabus_file or not syllabus_skills

if missing_resume or missing_syllabus:
    st.subheader("Some skills missing – help us fill the gaps")
    manual_skills = st.text_area(
        "List any technical skills you have (comma separated, e.g. Python, SQL, React, AWS)",
        value=", ".join(known_skills),
        height=100
    )
    known_skills = [s.strip() for s in manual_skills.split(",") if s.strip()]

    if not known_skills:
        st.warning("Please add some skills manually or upload documents properly")
        st.stop()

st.write("**Your known technical skills**:", ", ".join(known_skills[:20]) + "..." if len(known_skills) > 20 else ", ".join(known_skills))

# 3. Job role
st.subheader("Target Job Role")
common_roles = [
    "Select...",
    "SDE / Software Engineer Fresher",
    "Full Stack Developer",
    "Python Developer",
    "Data Analyst / Data Scientist",
    "Machine Learning Engineer",
    "Frontend Developer",
    "Backend Developer",
    "DevOps Engineer",
    "Other"
]

role = st.selectbox("Choose role", common_roles)

if role == "Other":
    role = st.text_input("Enter your target role")

if role and role != "Select...":
    with st.spinner(f"Preparing requirements for {role}..."):
        job_skills = generate_typical_job_skills(role)

    if job_skills:
        edited = st.text_area("Required skills for this role (edit if needed)", ", ".join(job_skills))
        job_skills = [s.strip() for s in edited.split(",") if s.strip()]

# 4. Interview Deadline
st.subheader("Interview Timeline")
interview_date = st.date_input("When is your interview/deadline? (optional)", value=None)

weeks_available = 8  # default
if interview_date:
    days = (interview_date - datetime.today().date()).days
    weeks_available = max(1, days // 7)
    st.info(f"Adjusting plan to {weeks_available} weeks based on your deadline")

# 5. Analyze
if st.button("Analyze Gaps & Generate Plan"):
    if not job_skills:
        st.error("Please select or enter a job role")
    else:
        gaps = compute_gaps(job_skills, known_skills)

        st.subheader(f"Gaps for {role}")
        if gaps:
            st.table(gaps)
        else:
            st.success("No major gaps detected!")

        st.subheader("Your Personalized Bridge Roadmap")
        roadmap = generate_roadmap(gaps, weeks=weeks_available)
        if roadmap:
            # Tree format using expanders
            for w in roadmap.get("roadmap", []):
                with st.expander(f"Week {w['week']} (Hours: {w['hours']})"):
                    for skill_rec in w.get('focus_skills', []):
                        if isinstance(skill_rec, list) and len(skill_rec) >= 2:
                            st.markdown(f"**Skill: {skill_rec[0]}**")
                            st.write(skill_rec[1])  # Recommendations
                        else:
                            st.markdown(f"**Skill: {skill_rec}**")
                    st.markdown("---")
        else:
            st.info("No roadmap needed (no gaps) or generation error")