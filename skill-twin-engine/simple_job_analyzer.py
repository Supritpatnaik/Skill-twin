"""
Simplified Job Market Analyzer - No TensorFlow Dependencies
Focus on web scraping and basic analysis
"""

import json
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import difflib

class SimpleJobMarketAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        
    def setup_headers(self):
        """Setup request headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session.headers.update(headers)
    
    def simple_skill_extractor(self, text: str) -> List[str]:
        """Simple skill extraction without AI"""
        if not text:
            return []
            
        # Common technical skills
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
    
    def mock_job_scraping(self, role: str) -> List[Dict]:
        """Mock job data for demonstration (since real scraping has dependency issues)"""
        mock_jobs = [
            {
                "title": f"{role} - Fresher",
                "company": "Tech Solutions Pvt Ltd",
                "location": "Bangalore",
                "description": f"Looking for fresh {role} graduates with Python, SQL, and web development skills. Must have good problem-solving abilities and understanding of data structures.",
                "url": "https://example.com/job1",
                "source": "Mock Data"
            },
            {
                "title": f"Junior {role}",
                "company": "Digital Innovations",
                "location": "Hyderabad", 
                "description": f"Entry-level {role} position. Required: Java, Spring Boot, REST APIs, MySQL. Freshers with strong academic background preferred.",
                "url": "https://example.com/job2",
                "source": "Mock Data"
            },
            {
                "title": f"{role} Trainee",
                "company": "Innovation Labs",
                "location": "Pune",
                "description": f"Training program for {role}. Skills needed: JavaScript, React, Node.js, MongoDB. No experience required, will provide training.",
                "url": "https://example.com/job3",
                "source": "Mock Data"
            }
        ]
        return mock_jobs
    
    def analyze_market_skills(self, role: str) -> Dict:
        """Analyze market skills for a role"""
        jobs = self.mock_job_scraping(role)
        all_skills = []
        
        for job in jobs:
            skills = self.simple_skill_extractor(job['description'])
            all_skills.extend(skills)
            job['extracted_skills'] = skills
        
        # Count skill frequency
        skill_count = {}
        for skill in all_skills:
            skill_lower = skill.lower()
            skill_count[skill_lower] = skill_count.get(skill_lower, 0) + 1
        
        # Sort by frequency
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        top_skills = [skill.title() for skill, count in sorted_skills[:15]]
        
        return {
            "role": role,
            "total_jobs": len(jobs),
            "top_skills": top_skills,
            "skill_frequency": dict(sorted_skills[:15]),
            "jobs": jobs
        }
    
    def compare_with_curriculum(self, market_skills: List[str], 
                              curriculum_skills: List[str]) -> Dict:
        """Compare market skills with curriculum"""
        # Simple string matching for similarity
        matches = []
        gaps = []
        
        for market_skill in market_skills:
            market_skill_lower = market_skill.lower()
            best_match = None
            best_ratio = 0
            
            for curriculum_skill in curriculum_skills:
                curriculum_skill_lower = curriculum_skill.lower()
                ratio = difflib.SequenceMatcher(None, market_skill_lower, curriculum_skill_lower).ratio()
                if ratio > best_ratio and ratio > 0.6:  # Threshold for match
                    best_ratio = ratio
                    best_match = curriculum_skill
            
            if best_match:
                matches.append({
                    "market_skill": market_skill,
                    "curriculum_match": best_match,
                    "similarity": round(best_ratio, 2)
                })
            else:
                gaps.append(market_skill)
        
        coverage = (len(matches) / len(market_skills)) * 100 if market_skills else 0
        
        return {
            "matches": matches,
            "gaps": gaps,
            "coverage_percentage": round(coverage, 2),
            "total_market_skills": len(market_skills),
            "covered_count": len(matches)
        }
    
    def generate_recommendations(self, gaps: List[str], student_skills: List[str]) -> List[Dict]:
        """Generate learning recommendations"""
        recommendations = []
        
        # Prioritize gaps based on frequency and importance
        priority_gaps = gaps[:10]  # Top 10 gaps
        
        for i, skill in enumerate(priority_gaps):
            priority = "High" if i < 3 else "Medium" if i < 7 else "Low"
            
            # Check if student already knows similar skills
            knows_similar = any(skill.lower() in s.lower() or s.lower() in skill.lower() 
                              for s in student_skills)
            
            recommendations.append({
                "skill": skill,
                "priority": priority,
                "category": "New Skill" if not knows_similar else "Enhancement",
                "resources": self.get_learning_resources(skill),
                "estimated_time": "2-4 weeks" if priority == "High" else "4-8 weeks",
                "prerequisites": self.get_prerequisites(skill)
            })
        
        return recommendations
    
    def get_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for a skill"""
        resource_map = {
            "Python": ["Python.org docs", "Automate the Boring Stuff", "Real Python"],
            "Java": ["Oracle Java Docs", "Java Programming tutorials", "Codecademy Java"],
            "JavaScript": ["MDN Web Docs", "JavaScript.info", "Eloquent JavaScript"],
            "React": ["React Official Docs", "React Tutorial", "Fullstack React"],
            "SQL": ["SQLBolt", "Mode Analytics", "W3Schools SQL"],
            "AWS": ["AWS Free Tier", "AWS Training", "A Cloud Guru"],
            "Docker": ["Docker Docs", "Docker Mastery", "Play with Docker"]
        }
        
        skill_lower = skill.lower().title()
        return resource_map.get(skill_lower, [f"Search {skill} tutorials on YouTube", f"{skill} official documentation"])
    
    def get_prerequisites(self, skill: str) -> List[str]:
        """Get prerequisites for a skill"""
        prereq_map = {
            "React": ["JavaScript", "HTML", "CSS"],
            "Docker": ["Linux basics", "Command line"],
            "Machine Learning": ["Python", "Statistics", "Mathematics"],
            "AWS": ["Cloud computing basics", "Networking fundamentals"]
        }
        
        skill_lower = skill.lower().title()
        return prereq_map.get(skill_lower, ["Basic programming knowledge"])

# Simple integration with existing app
class SimpleSkillTwinIntegration:
    def __init__(self):
        self.analyzer = SimpleJobMarketAnalyzer()
    
    def comprehensive_analysis(self, student_skills: List[str], 
                             target_role: str,
                             curriculum_skills: List[str]) -> Dict:
        """Complete analysis combining all components"""
        
        # Get market data
        market_data = self.analyzer.analyze_market_skills(target_role)
        market_skills = market_data['top_skills']
        
        # Compare with curriculum
        curriculum_comparison = self.analyzer.compare_with_curriculum(
            market_skills, curriculum_skills
        )
        
        # Identify student gaps
        student_gaps = []
        for market_skill in market_skills:
            # Simple check if student has this skill
            has_skill = any(market_skill.lower() in skill.lower() or 
                          skill.lower() in market_skill.lower() 
                          for skill in student_skills)
            if not has_skill:
                student_gaps.append(market_skill)
        
        # Generate recommendations
        recommendations = self.analyzer.generate_recommendations(
            student_gaps, student_skills
        )
        
        # Calculate student-market match
        total_market_skills = len(market_skills)
        student_matches = total_market_skills - len(student_gaps)
        student_match_percentage = (student_matches / total_market_skills) * 100 if total_market_skills > 0 else 0
        
        return {
            "student_profile": {
                "total_skills": len(student_skills),
                "skills_list": student_skills
            },
            "market_insights": {
                "role": target_role,
                "total_market_skills": total_market_skills,
                "top_skills": market_skills,
                "jobs_analyzed": market_data['total_jobs']
            },
            "curriculum_analysis": {
                "coverage": curriculum_comparison['coverage_percentage'],
                "covered_skills": curriculum_comparison['covered_count'],
                "missing_skills": len(curriculum_comparison['gaps'])
            },
            "student_analysis": {
                "match_percentage": round(student_match_percentage, 2),
                "gaps_count": len(student_gaps),
                "missing_skills": student_gaps[:15]
            },
            "recommendations": recommendations[:10]  # Top 10 recommendations
        }

# Test the simplified version
if __name__ == "__main__":
    # Load curriculum data
    with open('giet_cse_skills.json', 'r') as f:
        curriculum_data = json.load(f)
    
    curriculum_skills = curriculum_data['overall_technical_skills']
    student_skills = ["Python", "Java", "SQL", "Data Structures", "Algorithms"]
    target_role = "Software Developer"
    
    # Run analysis
    integration = SimpleSkillTwinIntegration()
    result = integration.comprehensive_analysis(
        student_skills, target_role, curriculum_skills
    )
    
    print("🎯 Skill-Twin Analysis Results")
    print("=" * 50)
    print(f"Target Role: {result['market_insights']['role']}")
    print(f"Student Skills: {result['student_profile']['total_skills']}")
    print(f"Market Match: {result['student_analysis']['match_percentage']}%")
    print(f"Curriculum Coverage: {result['curriculum_analysis']['coverage']}%")
    
    print(f"\n📋 Top Market Skills:")
    for skill in result['market_insights']['top_skills'][:10]:
        print(f"  • {skill}")
    
    print(f"\n⚠️ Skills You Need to Learn:")
    for skill in result['student_analysis']['missing_skills'][:8]:
        print(f"  • {skill}")
    
    print(f"\n📚 Learning Recommendations:")
    for rec in result['recommendations'][:5]:
        print(f"  • {rec['skill']} ({rec['priority']} priority) - {rec['estimated_time']}")