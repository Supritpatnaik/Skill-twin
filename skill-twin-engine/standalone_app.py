"""
Standalone Skill-Twin App - No External Dependencies
Complete web application with job market analysis
"""

import streamlit as st
import json
import difflib
from typing import List, Dict
import time

# Simple skill analyzer without external dependencies
class StandaloneSkillAnalyzer:
    def __init__(self):
        pass
    
    def simple_skill_extractor(self, text: str) -> List[str]:
        """Extract skills using simple keyword matching"""
        if not text:
            return []
            
        # Common technical skills database
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'linux', 'spring', 'django', 'flask',
            'tensorflow', 'pytorch', 'machine learning', 'data science', 'api',
            'rest', 'graphql', 'html', 'css', 'bootstrap', 'jquery', 'typescript',
            'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'php', 'ruby'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def mock_job_market_data(self, role: str) -> Dict:
        """Generate mock job market data"""
        # Role-specific skill requirements
        role_skills = {
            "Software Developer": ["Python", "Java", "JavaScript", "SQL", "Git", "REST API", "Spring", "React"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "MongoDB", "HTML", "CSS", "REST API", "Git"],
            "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "NumPy", "R"],
            "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD", "Git", "Python"]
        }
        
        # Default to general skills if role not found
        market_skills = role_skills.get(role, ["Python", "Java", "SQL", "JavaScript"])
        
        return {
            "role": role,
            "market_skills": market_skills,
            "total_jobs": 50,
            "average_salary": "₹4-8 Lakhs"
        }
    
    def calculate_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skills"""
        return difflib.SequenceMatcher(None, skill1.lower(), skill2.lower()).ratio()
    
    def analyze_gaps(self, student_skills: List[str], market_skills: List[str]) -> Dict:
        """Analyze gaps between student and market requirements"""
        gaps = []
        matches = []
        
        for market_skill in market_skills:
            best_match = None
            best_similarity = 0
            
            for student_skill in student_skills:
                similarity = self.calculate_similarity(market_skill, student_skill)
                if similarity > best_similarity and similarity > 0.6:
                    best_similarity = similarity
                    best_match = student_skill
            
            if best_match:
                matches.append({
                    "market_skill": market_skill,
                    "student_skill": best_match,
                    "similarity": round(best_similarity, 2)
                })
            else:
                gaps.append({
                    "skill": market_skill,
                    "urgency": "High" if market_skill in market_skills[:5] else "Medium"
                })
        
        match_percentage = (len(matches) / len(market_skills)) * 100 if market_skills else 0
        
        return {
            "matches": matches,
            "gaps": gaps,
            "match_percentage": round(match_percentage, 2),
            "total_market_skills": len(market_skills),
            "covered_count": len(matches)
        }
    
    def generate_recommendations(self, gaps: List[Dict], student_skills: List[str]) -> List[Dict]:
        """Generate learning recommendations"""
        recommendations = []
        
        # Priority mapping for common skills
        priority_map = {
            "Python": "High",
            "JavaScript": "High", 
            "SQL": "High",
            "React": "Medium",
            "Node.js": "Medium",
            "Docker": "Medium",
            "AWS": "Low",
            "Machine Learning": "Low"
        }
        
        for gap in gaps[:10]:  # Top 10 gaps
            skill = gap['skill']
            priority = priority_map.get(skill, gap['urgency'])
            
            # Check if student has related skills
            has_related = any(self.calculate_similarity(skill, s) > 0.7 for s in student_skills)
            
            recommendations.append({
                "skill": skill,
                "priority": priority,
                "category": "New Skill" if not has_related else "Enhancement",
                "estimated_time": "2-4 weeks" if priority == "High" else "4-8 weeks",
                "resources": self.get_resources(skill)
            })
        
        return recommendations
    
    def get_resources(self, skill: str) -> List[str]:
        """Get learning resources for a skill"""
        resource_map = {
            "Python": ["Python.org docs", "Automate the Boring Stuff", "Real Python"],
            "JavaScript": ["MDN Web Docs", "JavaScript.info", "Eloquent JavaScript"],
            "SQL": ["SQLBolt", "Mode Analytics", "W3Schools SQL"],
            "React": ["React Official Docs", "React Tutorial", "Fullstack React"],
            "Node.js": ["Node.js Docs", "Express.js Guide", "Node Hero"],
            "Docker": ["Docker Docs", "Docker Mastery", "Play with Docker"],
            "AWS": ["AWS Free Tier", "AWS Training", "A Cloud Guru"]
        }
        
        return resource_map.get(skill, [f"{skill} official documentation", f"Search {skill} tutorials on YouTube"])

# Main Streamlit App
def main():
    st.set_page_config(page_title="Skill-Twin Engine", page_icon="🎓", layout="wide")
    
    st.title("🎓 Skill-Twin Engine")
    st.markdown("Upload your resume and/or syllabus → choose job role → get gaps & customized plan")
    
    # Initialize analyzer
    analyzer = StandaloneSkillAnalyzer()
    
    # Load curriculum data
    try:
        with open('giet_cse_skills.json', 'r') as f:
            curriculum_data = json.load(f)
        curriculum_skills = curriculum_data['overall_technical_skills']
    except FileNotFoundError:
        st.error("Curriculum data file not found!")
        curriculum_skills = []
    
    # 1. User basic info
    st.subheader("👤 Your Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
    with col2:
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "ME", "CE", "Other"])
    
    year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th"])
    
    # 2. Skills input
    st.subheader("🛠️ Your Skills")
    skills_input = st.text_area(
        "Enter your technical skills (comma separated)",
        placeholder="e.g., Python, Java, SQL, Data Structures, Machine Learning",
        height=100
    )
    
    if skills_input:
        student_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        st.success(f"✅ Loaded {len(student_skills)} skills")
    else:
        student_skills = []
        st.warning("Please enter your skills")
    
    # 3. Job role selection
    st.subheader("🎯 Target Job Role")
    common_roles = [
        "Software Developer",
        "Full Stack Developer", 
        "Data Scientist",
        "Machine Learning Engineer",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Python Developer"
    ]
    
    role = st.selectbox("Choose your target role", common_roles)
    
    # 4. Job Market Analysis Section
    st.subheader("📊 Live Job Market Insights")
    
    if st.checkbox("Include job market analysis"):
        if st.button("🔍 Analyze Job Market"):
            with st.spinner("Analyzing current job market..."):
                # Get market data
                market_data = analyzer.mock_job_market_data(role)
                market_skills = market_data['market_skills']
                
                # Analyze gaps
                gap_analysis = analyzer.analyze_gaps(student_skills, market_skills)
                
                # Generate recommendations
                recommendations = analyzer.generate_recommendations(
                    gap_analysis['gaps'], student_skills
                )
                
                # Store in session state
                st.session_state.analysis_results = {
                    "market_data": market_data,
                    "gap_analysis": gap_analysis,
                    "recommendations": recommendations
                }
                
                st.success("✅ Job market analysis complete!")
    
    # 5. Display Results
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        
        # Summary metrics
        st.subheader(f"🎯 Analysis Results for {role}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Your Skills", len(student_skills))
        with col2:
            st.metric("Market Match", f"{results['gap_analysis']['match_percentage']}%")
        with col3:
            st.metric("Skills to Learn", len(results['gap_analysis']['gaps']))
        with col4:
            st.metric("Market Skills", results['gap_analysis']['total_market_skills'])
        
        # Detailed analysis
        tab1, tab2, tab3, tab4 = st.tabs(["Market Insights", "Your Gaps", "Recommendations", "Curriculum"])
        
        with tab1:
            st.write(f"**Role:** {results['market_data']['role']}")
            st.write(f"**Jobs Available:** {results['market_data']['total_jobs']}")
            st.write(f"**Average Salary:** {results['market_data']['average_salary']}")
            
            st.write("**Top Market Skills:**")
            for i, skill in enumerate(results['market_data']['market_skills'][:10], 1):
                st.write(f"{i}. {skill}")
        
        with tab2:
            if results['gap_analysis']['gaps']:
                st.write("**Skills you need to develop:**")
                for gap in results['gap_analysis']['gaps'][:10]:
                    st.write(f"• **{gap['skill']}** (Priority: {gap['urgency']})")
            else:
                st.success("🎉 Excellent! No major skill gaps detected.")
        
        with tab3:
            st.write("**Personalized Learning Plan:**")
            for i, rec in enumerate(results['recommendations'][:8], 1):
                st.markdown(f"**{i}. {rec['skill']}** ({rec['priority']} priority)")
                st.write(f"   Category: {rec['category']}")
                st.write(f"   Time needed: {rec['estimated_time']}")
                st.write(f"   Resources: {', '.join(rec['resources'][:2])}")
                st.markdown("---")
        
        with tab4:
            st.write(f"**University Curriculum Coverage:**")
            st.write(f"Total curriculum skills: {len(curriculum_skills)}")
            
            # Compare curriculum with market
            curriculum_matches = []
            for market_skill in results['market_data']['market_skills']:
                for curriculum_skill in curriculum_skills:
                    if analyzer.calculate_similarity(market_skill, curriculum_skill) > 0.6:
                        curriculum_matches.append((market_skill, curriculum_skill))
                        break
            
            coverage = (len(curriculum_matches) / len(results['market_data']['market_skills'])) * 100
            st.metric("Curriculum Coverage", f"{round(coverage, 1)}%")
            
            if curriculum_matches:
                st.write("**Skills covered by curriculum:**")
                for market_skill, curriculum_skill in curriculum_matches[:10]:
                    st.write(f"• {market_skill} ← {curriculum_skill}")

if __name__ == "__main__":
    main()