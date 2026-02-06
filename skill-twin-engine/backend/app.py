from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, random
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import pdfplumber

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Models
# Note: For production, handle api_key check more gracefully
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Mapping subject names to your JSON files
SUBJECT_MAP = {
    "Python": "python.json", 
    "DSA": "dsa.json", 
    "Communication": "communication.json", 
    "SQL": "sql.json"
}

# ---------------------------------------------------------------------
# Helper Functions (Ported from Streamlit app.py)
# ---------------------------------------------------------------------

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
        print(f"Skill extraction error: {e}")
        return []

def validate_skills(extracted_skills):
    # Common technical skills database for validation
    trusted_skills_db = set([
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "Go", "Rust", "Swift", "Kotlin", "PHP",
        "React", "Angular", "Vue.js", "Svelte", "Django", "Flask", "FastAPI", "Spring", "Node.js", 
        "Express", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Bootstrap", "jQuery",
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab CI", "Terraform",
        "Git", "Linux", "Bash", "REST API", "GraphQL", "API", "CI/CD", "Agile", "Scrum",
        "Machine Learning", "Deep Learning", "Data Science", "AI", "NLP", "Computer Vision",
        "Cybersecurity", "DevOps", "Microservices", "Testing", "JUnit", "Selenium"
    ])
    
    validated_skills = []
    uncertain_skills = []
    
    for skill in extracted_skills:
        normalized_skill = skill.strip().lower()
        if normalized_skill in [s.lower() for s in trusted_skills_db]:
            validated_skills.append(skill)
        else:
            is_valid = False
            for trusted_skill in trusted_skills_db:
                if normalized_skill.replace(" ", "") == trusted_skill.replace(" ", "").lower():
                    validated_skills.append(skill)
                    is_valid = True
                    break
            if not is_valid:
                uncertain_skills.append(skill)
    
    return validated_skills, uncertain_skills

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
    
    # If using remote embeddings, ensuring they are lists of strings
    job_emb = embedder.encode(job_skills)
    known_emb = embedder.encode(known_skills)
    
    gaps = []
    for i, skill in enumerate(job_skills):
        sims = util.cos_sim(job_emb[i], known_emb)[0]
        best = sims.max().item()
        
        # Threshold logic from original app
        if best < 0.55:
            gaps.append({
                "skill": skill,
                "match": round(best, 2),
                "level": "High" if best < 0.4 else "Medium"
            })
    return sorted(gaps, key=lambda x: x["match"])

def generate_roadmap(gaps, weeks=8):
    if not gaps:
        return {}
        
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
          "focus_skills": [["Docker basics", "Recommendations: ..."]],
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

# ---------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------

@app.route('/api/questions', methods=['POST'])
def get_questions():
    try:
        selected_subjects = request.json.get('subjects', [])
        final_quiz = []
        for sub in selected_subjects:
            filename = SUBJECT_MAP.get(sub)
            if filename and os.path.exists(filename):
                with open(filename, 'r') as f:
                    data = json.load(f)
                    unique = list({q['question'].strip().lower(): q for q in data}.values())
                    sampled = random.sample(unique, min(len(unique), 10))
                    for s_q in sampled: s_q['subject'] = sub
                    final_quiz.extend(sampled)
        
        random.shuffle(final_quiz)
        return jsonify(final_quiz)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        results = data.get('results', [])
        
        stats = {}
        for r in results:
            sub = r['subject']
            if sub not in stats: stats[sub] = {"correct": 0, "total": 0}
            stats[sub]["total"] += 1
            if r['isCorrect']: stats[sub]["correct"] += 1

        graph_data = [{"subject": k, "score": round((v['correct']/v['total'])*100)} for k, v in stats.items()]
        strong = [s for s, v in stats.items() if (v['correct']/v['total']) >= 0.7]
        weak = [s for s, v in stats.items() if (v['correct']/v['total']) < 0.7]

        plan = {}
        for i in range(1, 8):
            focus = weak[i % len(weak)] if weak else "Advanced System Design"
            plan[f"Day {i}"] = f"Intensive deep-dive into {focus} logic and implementation."

        return jsonify({
            "graph_data": graph_data,
            "ai_analysis": {
                "strengths": strong if strong else ["Basic Syntax"],
                "weaknesses": weak if weak else ["Advanced Optimization"],
                "suggestions": [f"Focus on {w} projects" for w in weak] + ["Review mock interview patterns"]
            },
            "seven_day_plan": plan
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parses uploaded PDF and returns extracted skills."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages if page.extract_text())
        
        extracted_skills = extract_skills(text, "resume")
        validated, uncertain = validate_skills(extracted_skills)
        
        return jsonify({
            "extracted_skills": extracted_skills,
            "validated_skills": validated,
            "uncertain_skills": uncertain
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/job-requirements', methods=['POST'])
def job_requirements():
    """Generates required skills for a given job role."""
    data = request.json
    role = data.get('role')
    if not role:
        return jsonify({"error": "Role is required"}), 400
        
    skills = generate_typical_job_skills(role)
    return jsonify({"required_skills": skills})

@app.route('/api/analyze-gaps', methods=['POST'])
def analyze_gaps():
    """Computes gaps between known skills and job skills."""
    data = request.json
    known_skills = data.get('known_skills', [])
    job_skills = data.get('job_skills', [])
    
    gaps = compute_gaps(job_skills, known_skills)
    return jsonify({"gaps": gaps})

@app.route('/api/generate-roadmap', methods=['POST'])
def generate_roadmap_api():
    """Generates a study roadmap based on gaps."""
    data = request.json
    gaps = data.get('gaps', [])
    weeks = data.get('weeks', 8)
    
    roadmap = generate_roadmap(gaps, weeks)
    return jsonify({"roadmap": roadmap})

def find_resources(query):
    prompt = f"""
    Find 4-6 high-quality learning resources for: "{query}"
    Include a mix of YouTube, Coursera/Udemy (paid but popular), and free documentation/articles.
    Output strict JSON format:
    {{
        "resources": [
            {{
                "skill": "{query}", 
                "resources": [
                    {{ "platform": "YouTube", "title": "Crash Course...", "url": "...", "isFree": true }},
                    {{ "platform": "Coursera", "title": "Specialization...", "url": "...", "isFree": false }}
                ]
            }}
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
    except Exception as e:
        print(f"Resource finding error: {e}")
        return {"resources": []}

@app.route('/api/find-resources', methods=['POST'])
def find_learning_resources():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    result = find_resources(query)
    return jsonify({"success": True, "resources": result.get("resources", [])})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
