"""
Job Market Integration Module for Skill-Twin Engine
Connects job scraping functionality with gap analysis
"""

import json
import os
from typing import List, Dict, Optional
from job_scraper import JobScraper
from advanced_job_scraper import AdvancedJobScraper
from sentence_transformers import SentenceTransformer, util
import numpy as np

class JobMarketAnalyzer:
    def __init__(self):
        self.job_scraper = JobScraper()
        self.advanced_scraper = AdvancedJobScraper()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def get_current_job_market_skills(self, role: str, location: str = "India", 
                                    use_advanced: bool = True) -> Dict:
        """
        Get current market skills for a specific role
        """
        try:
            if use_advanced:
                market_data = self.advanced_scraper.aggregate_job_data(role, location, limit=20)
                skills = market_data['market_insights']['top_skills']
            else:
                job_data = self.job_scraper.get_job_skills_for_role(role, location, limit=10)
                skills = job_data['top_skills']
                
            return {
                "role": role,
                "location": location,
                "skills": skills,
                "source": "advanced_scraper" if use_advanced else "basic_scraper",
                "timestamp": str(int(time.time())) if 'time' in globals() else "current"
            }
        except Exception as e:
            print(f"Error getting market skills: {e}")
            return {"role": role, "skills": [], "error": str(e)}
    
    def compare_with_university_curriculum(self, job_skills: List[str], 
                                         curriculum_skills: List[str]) -> Dict:
        """
        Compare job market skills with university curriculum
        """
        if not job_skills or not curriculum_skills:
            return {"gap_analysis": [], "coverage": 0}
        
        # Create embeddings
        job_embeddings = self.embedder.encode(job_skills)
        curriculum_embeddings = self.embedder.encode(curriculum_skills)
        
        # Calculate similarities
        similarities = util.cos_sim(job_embeddings, curriculum_embeddings)
        
        gap_analysis = []
        covered_count = 0
        
        for i, job_skill in enumerate(job_skills):
            max_sim = float(similarities[i].max())
            best_match_idx = int(similarities[i].argmax())
            best_match = curriculum_skills[best_match_idx]
            
            # Determine gap level
            if max_sim >= 0.7:
                gap_level = "Covered"
                covered_count += 1
            elif max_sim >= 0.5:
                gap_level = "Partially Covered"
            else:
                gap_level = "Not Covered"
            
            gap_analysis.append({
                "job_skill": job_skill,
                "best_curriculum_match": best_match,
                "similarity": round(max_sim, 3),
                "gap_level": gap_level
            })
        
        coverage_percentage = (covered_count / len(job_skills)) * 100 if job_skills else 0
        
        return {
            "gap_analysis": gap_analysis,
            "coverage_percentage": round(coverage_percentage, 2),
            "total_job_skills": len(job_skills),
            "covered_skills": covered_count,
            "missing_skills": len(job_skills) - covered_count
        }
    
    def generate_market_insights_report(self, role: str, curriculum_skills: List[str],
                                      location: str = "India") -> Dict:
        """
        Generate comprehensive market insights report
        """
        # Get current market skills
        market_data = self.get_current_job_market_skills(role, location, use_advanced=True)
        job_skills = market_data.get('skills', [])
        
        if not job_skills:
            return {"error": "Could not fetch job market data"}
        
        # Compare with curriculum
        gap_analysis = self.compare_with_university_curriculum(job_skills, curriculum_skills)
        
        # Identify critical gaps
        missing_skills = [item['job_skill'] for item in gap_analysis['gap_analysis'] 
                         if item['gap_level'] == 'Not Covered']
        
        partially_covered = [item['job_skill'] for item in gap_analysis['gap_analysis'] 
                           if item['gap_level'] == 'Partially Covered']
        
        report = {
            "executive_summary": {
                "role": role,
                "location": location,
                "curriculum_coverage": f"{gap_analysis['coverage_percentage']}%",
                "total_market_skills": gap_analysis['total_job_skills'],
                "skills_covered": gap_analysis['covered_skills'],
                "skills_missing": gap_analysis['missing_skills']
            },
            "market_skills": job_skills[:20],  # Top 20 skills
            "critical_gaps": missing_skills[:15],  # Top 15 missing skills
            "partial_coverage": partially_covered[:10],  # Top 10 partially covered
            "detailed_analysis": gap_analysis['gap_analysis'],
            "recommendations": self.generate_recommendations(missing_skills, partially_covered)
        }
        
        return report
    
    def generate_recommendations(self, missing_skills: List[str], 
                               partially_covered: List[str]) -> List[Dict]:
        """
        Generate specific recommendations for curriculum improvement
        """
        recommendations = []
        
        # Prioritize recommendations based on frequency and importance
        priority_skills = missing_skills[:8] + partially_covered[:5]
        
        for i, skill in enumerate(priority_skills):
            priority = "High" if i < 5 else "Medium" if i < 10 else "Low"
            
            recommendations.append({
                "skill": skill,
                "priority": priority,
                "category": "Missing" if skill in missing_skills else "Enhancement",
                "suggested_action": f"Add {skill} to curriculum or increase focus",
                "implementation_quarter": "Q1-2026" if priority == "High" else "Q2-2026"
            })
        
        return recommendations

# Integration with existing Skill-Twin engine
class IntegratedSkillTwin:
    def __init__(self):
        self.job_analyzer = JobMarketAnalyzer()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def analyze_student_with_market_data(self, student_skills: List[str], 
                                       target_role: str,
                                       curriculum_skills: List[str],
                                       location: str = "India") -> Dict:
        """
        Complete analysis combining student skills, job market, and curriculum
        """
        # Get market data
        market_report = self.job_analyzer.generate_market_insights_report(
            target_role, curriculum_skills, location
        )
        
        if "error" in market_report:
            return market_report
        
        # Analyze student vs market
        job_skills = market_report['market_skills']
        job_embeddings = self.embedder.encode(job_skills)
        student_embeddings = self.embedder.encode(student_skills)
        
        # Calculate student-job match
        if len(student_skills) > 0:
            similarities = util.cos_sim(job_embeddings, student_embeddings)
            student_match_scores = similarities.max(dim=1).values
            avg_match = float(student_match_scores.mean())
        else:
            avg_match = 0.0
        
        # Identify student gaps
        student_gaps = []
        for i, job_skill in enumerate(job_skills[:15]):  # Top 15 skills
            if len(student_skills) > 0:
                max_sim = float(similarities[i].max())
                if max_sim < 0.6:  # Threshold for gap
                    student_gaps.append({
                        "skill": job_skill,
                        "match_score": round(max_sim, 3),
                        "urgency": "High" if max_sim < 0.4 else "Medium"
                    })
        
        # Combine all insights
        comprehensive_analysis = {
            "student_profile": {
                "total_skills": len(student_skills),
                "skills_list": student_skills[:20]
            },
            "market_insights": market_report,
            "student_market_match": {
                "overall_match_percentage": round(avg_match * 100, 2),
                "gaps_identified": len(student_gaps),
                "top_gaps": student_gaps
            },
            "personalized_recommendations": self.generate_student_recommendations(
                student_gaps, market_report['critical_gaps']
            )
        }
        
        return comprehensive_analysis
    
    def generate_student_recommendations(self, student_gaps: List[Dict], 
                                       market_gaps: List[str]) -> List[Dict]:
        """
        Generate personalized learning recommendations for student
        """
        recommendations = []
        
        # Focus on student's specific gaps
        for gap in student_gaps[:8]:  # Top 8 gaps
            recommendations.append({
                "skill": gap['skill'],
                "priority": gap['urgency'],
                "type": "Immediate Learning Need",
                "resources": self.suggest_learning_resources(gap['skill']),
                "estimated_time": "2-4 weeks",
                "impact": "High - directly improves job market match"
            })
        
        # Add market-critical skills
        for skill in market_gaps[:5]:
            if skill not in [g['skill'] for g in student_gaps]:
                recommendations.append({
                    "skill": skill,
                    "priority": "Medium",
                    "type": "Market Trend Skill",
                    "resources": self.suggest_learning_resources(skill),
                    "estimated_time": "3-6 weeks",
                    "impact": "Medium - improves competitiveness"
                })
        
        return recommendations
    
    def suggest_learning_resources(self, skill: str) -> List[str]:
        """
        Suggest learning resources for a specific skill
        """
        resource_map = {
            "python": ["Python.org documentation", "Automate the Boring Stuff", "Real Python tutorials"],
            "javascript": ["MDN Web Docs", "JavaScript.info", "Eloquent JavaScript"],
            "react": ["React official docs", "React Tutorial by Scrimba", "Fullstack React"],
            "sql": ["SQLBolt", "Mode Analytics SQL Tutorial", "W3Schools SQL"],
            "aws": ["AWS Free Tier", "AWS Training and Certification", "A Cloud Guru"],
            "docker": ["Docker Docs", "Docker Mastery course", "Play with Docker"],
            "machine learning": ["Andrew Ng's ML Course", "Kaggle Learn", "Hands-on ML book"],
            "data science": ["DataCamp", "Kaggle", "Python for Data Analysis book"]
        }
        
        skill_lower = skill.lower()
        for key, resources in resource_map.items():
            if key in skill_lower:
                return resources
        
        # Default resources
        return [
            f"Search for {skill} tutorials on YouTube",
            f"Check {skill} documentation",
            f"Find {skill} courses on Coursera/edX"
        ]

# Example usage
if __name__ == "__main__":
    import time
    
    # Load curriculum data
    with open('giet_cse_skills.json', 'r') as f:
        curriculum_data = json.load(f)
    
    curriculum_skills = curriculum_data['overall_technical_skills']
    
    # Sample student skills
    student_skills = ["Python", "Java", "SQL", "Data Structures", "Algorithms"]
    
    # Initialize integrated system
    skill_twin = IntegratedSkillTwin()
    
    # Analyze student for a target role
    target_role = "Full Stack Developer"
    analysis = skill_twin.analyze_student_with_market_data(
        student_skills, target_role, curriculum_skills
    )
    
    print(f"\n🎓 Comprehensive Skill-Twin Analysis for: {target_role}")
    print(f"Student skills: {analysis['student_profile']['total_skills']}")
    print(f"Market coverage: {analysis['market_insights']['executive_summary']['curriculum_coverage']}")
    print(f"Student-market match: {analysis['student_market_match']['overall_match_percentage']}%")
    
    print(f"\n🎯 Top Skills to Learn:")
    for rec in analysis['personalized_recommendations'][:5]:
        print(f"- {rec['skill']} ({rec['priority']} priority): {rec['estimated_time']}")
    
    # Save analysis
    with open('comprehensive_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)