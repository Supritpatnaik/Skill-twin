"""
Real Job Market Integration for Skill-Twin Engine
Connects real job scraping with gap analysis
"""

import json
import time
from typing import List, Dict
from real_job_scraper import RealJobScraper
import difflib

class RealJobMarketAnalyzer:
    def __init__(self):
        self.job_scraper = RealJobScraper()
        
    def get_current_job_market_skills(self, role: str, location: str = "India") -> Dict:
        """
        Get current market skills by scraping real job portals
        """
        try:
            market_data = self.job_scraper.aggregate_job_data(role, location, limit=25)
            skills = market_data['market_insights']['top_skills']
            
            return {
                "role": role,
                "location": location,
                "skills": skills,
                "skill_frequency": market_data['market_insights']['skill_frequency'],
                "total_jobs": market_data['aggregation']['total_jobs_found'],
                "sources": market_data['aggregation']['sources_used'],
                "raw_data": market_data,
                "timestamp": int(time.time())
            }
        except Exception as e:
            print(f"Error getting real market skills: {e}")
            return {"role": role, "skills": [], "error": str(e)}
    
    def compare_with_curriculum(self, market_skills: List[str], 
                              curriculum_skills: List[str]) -> Dict:
        """
        Compare real market skills with university curriculum
        """
        if not market_skills or not curriculum_skills:
            return {"gap_analysis": [], "coverage": 0}
        
        gap_analysis = []
        covered_count = 0
        
        for market_skill in market_skills:
            best_match = None
            best_similarity = 0
            
            # Find best matching curriculum skill
            for curriculum_skill in curriculum_skills:
                similarity = difflib.SequenceMatcher(
                    None, 
                    market_skill.lower(), 
                    curriculum_skill.lower()
                ).ratio()
                
                if similarity > best_similarity and similarity > 0.6:
                    best_similarity = similarity
                    best_match = curriculum_skill
            
            # Determine gap level
            if best_similarity >= 0.8:
                gap_level = "Well Covered"
                covered_count += 1
            elif best_similarity >= 0.6:
                gap_level = "Partially Covered"
            else:
                gap_level = "Not Covered"
            
            gap_analysis.append({
                "market_skill": market_skill,
                "best_curriculum_match": best_match if best_match else "No match",
                "similarity": round(best_similarity, 3),
                "gap_level": gap_level
            })
        
        coverage_percentage = (covered_count / len(market_skills)) * 100 if market_skills else 0
        
        return {
            "gap_analysis": gap_analysis,
            "coverage_percentage": round(coverage_percentage, 2),
            "total_market_skills": len(market_skills),
            "covered_skills": covered_count,
            "partially_covered": len([g for g in gap_analysis if g['gap_level'] == 'Partially Covered']),
            "missing_skills": len([g for g in gap_analysis if g['gap_level'] == 'Not Covered'])
        }
    
    def generate_real_market_report(self, role: str, curriculum_skills: List[str],
                                  location: str = "India") -> Dict:
        """
        Generate comprehensive real market insights report
        """
        # Get real market data
        market_data = self.get_current_job_market_skills(role, location)
        
        if "error" in market_data:
            return {"error": f"Could not fetch real job market data: {market_data['error']}"}
        
        market_skills = market_data['skills']
        
        if not market_skills:
            return {"error": "No market skills found"}
        
        # Compare with curriculum
        gap_analysis = self.compare_with_curriculum(market_skills, curriculum_skills)
        
        # Identify critical gaps
        missing_skills = [item['market_skill'] for item in gap_analysis['gap_analysis'] 
                         if item['gap_level'] == 'Not Covered']
        
        partially_covered = [item['market_skill'] for item in gap_analysis['gap_analysis'] 
                           if item['gap_level'] == 'Partially Covered']
        
        # Get skill frequency data
        skill_frequency = market_data.get('skill_frequency', {})
        
        report = {
            "executive_summary": {
                "role": role,
                "location": location,
                "total_jobs_analyzed": market_data['total_jobs'],
                "sources_used": market_data['sources'],
                "curriculum_coverage": f"{gap_analysis['coverage_percentage']}%",
                "total_market_skills": gap_analysis['total_market_skills'],
                "skills_covered": gap_analysis['covered_skills'],
                "skills_partially_covered": gap_analysis['partially_covered'],
                "skills_missing": gap_analysis['missing_skills']
            },
            "market_skills": {
                "top_skills": market_skills[:20],
                "skill_frequency": {skill: skill_frequency.get(skill.lower(), 0) 
                                  for skill in market_skills[:20]}
            },
            "gap_analysis": {
                "critical_gaps": missing_skills[:15],
                "partial_coverage": partially_covered[:10],
                "detailed_analysis": gap_analysis['gap_analysis']
            },
            "recommendations": self.generate_curriculum_recommendations(
                missing_skills, partially_covered
            ),
            "raw_job_data": market_data['raw_data']
        }
        
        return report
    
    def generate_curriculum_recommendations(self, missing_skills: List[str], 
                                          partially_covered: List[str]) -> List[Dict]:
        """
        Generate recommendations for curriculum improvement
        """
        recommendations = []
        
        # Prioritize based on market demand
        priority_skills = missing_skills[:10] + partially_covered[:8]
        
        for i, skill in enumerate(priority_skills):
            priority = "High" if i < 6 else "Medium" if i < 12 else "Low"
            category = "Missing Skill" if skill in missing_skills else "Enhancement Needed"
            
            recommendations.append({
                "skill": skill,
                "priority": priority,
                "category": category,
                "suggested_action": f"Add {skill} to curriculum or increase course hours",
                "implementation_quarter": "Q1-2026" if priority == "High" else "Q2-2026",
                "estimated_impact": "High - addresses critical market gap" if priority == "High" 
                                  else "Medium - improves competitiveness"
            })
        
        return recommendations

class RealSkillTwinIntegration:
    def __init__(self):
        self.job_analyzer = RealJobMarketAnalyzer()
        
    def comprehensive_real_analysis(self, student_skills: List[str], 
                                  target_role: str,
                                  curriculum_skills: List[str],
                                  location: str = "India") -> Dict:
        """
        Complete analysis combining real student skills, job market, and curriculum
        """
        # Get real market data
        market_report = self.job_analyzer.generate_real_market_report(
            target_role, curriculum_skills, location
        )
        
        if "error" in market_report:
            return market_report
        
        # Analyze student vs real market
        market_skills = market_report['market_skills']['top_skills']
        
        # Calculate student-market match
        student_matches = 0
        student_gaps = []
        
        for market_skill in market_skills[:15]:  # Top 15 market skills
            best_match = None
            best_similarity = 0
            
            for student_skill in student_skills:
                similarity = difflib.SequenceMatcher(
                    None,
                    market_skill.lower(),
                    student_skill.lower()
                ).ratio()
                
                if similarity > best_similarity and similarity > 0.6:
                    best_similarity = similarity
                    best_match = student_skill
            
            if best_match and best_similarity >= 0.7:
                student_matches += 1
            else:
                urgency = "High" if market_skill in market_skills[:8] else "Medium"
                student_gaps.append({
                    "skill": market_skill,
                    "match_score": round(best_similarity, 3),
                    "urgency": urgency
                })
        
        student_match_percentage = (student_matches / len(market_skills[:15])) * 100 if market_skills else 0
        
        # Combine all insights
        comprehensive_analysis = {
            "student_profile": {
                "total_skills": len(student_skills),
                "skills_list": student_skills[:20]
            },
            "real_market_insights": market_report,
            "student_market_analysis": {
                "overall_match_percentage": round(student_match_percentage, 2),
                "gaps_identified": len(student_gaps),
                "top_gaps": student_gaps
            },
            "personalized_recommendations": self.generate_student_recommendations(
                student_gaps, 
                market_report['gap_analysis']['critical_gaps']
            )
        }
        
        return comprehensive_analysis
    
    def generate_student_recommendations(self, student_gaps: List[Dict], 
                                       market_gaps: List[str]) -> List[Dict]:
        """
        Generate personalized learning recommendations for student based on real market data
        """
        recommendations = []
        
        # Focus on student's specific gaps
        for gap in student_gaps[:10]:  # Top 10 gaps
            recommendations.append({
                "skill": gap['skill'],
                "priority": gap['urgency'],
                "type": "Immediate Learning Need",
                "resources": self.suggest_learning_resources(gap['skill']),
                "estimated_time": "2-4 weeks" if gap['urgency'] == "High" else "4-8 weeks",
                "market_demand": f"High - appears in {len([j for j in self.get_recent_jobs(gap['skill'])][:5])} recent job postings",
                "impact": "High - directly improves job market competitiveness"
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
                    "market_demand": f"Medium - growing demand in {len([j for j in self.get_recent_jobs(skill)][:3])}+ companies",
                    "impact": "Medium - improves long-term career prospects"
                })
        
        return recommendations
    
    def get_recent_jobs(self, skill: str) -> List[Dict]:
        """
        Get recent jobs that mention a specific skill (placeholder for real implementation)
        """
        # This would connect to a job database or API
        # For now, return mock data
        return [
            {"title": f"{skill} Developer", "company": "Tech Corp", "posted": "2 days ago"},
            {"title": f"Junior {skill} Engineer", "company": "Innovations Ltd", "posted": "1 week ago"}
        ]
    
    def suggest_learning_resources(self, skill: str) -> List[str]:
        """
        Suggest learning resources for a specific skill
        """
        resource_map = {
            "Python": ["Python.org documentation", "Automate the Boring Stuff", "Real Python tutorials"],
            "JavaScript": ["MDN Web Docs", "JavaScript.info", "Eloquent JavaScript"],
            "React": ["React official docs", "React Tutorial by Scrimba", "Fullstack React"],
            "SQL": ["SQLBolt", "Mode Analytics SQL Tutorial", "W3Schools SQL"],
            "AWS": ["AWS Free Tier", "AWS Training and Certification", "A Cloud Guru"],
            "Docker": ["Docker Docs", "Docker Mastery course", "Play with Docker"],
            "Machine Learning": ["Andrew Ng's ML Course", "Kaggle Learn", "Hands-on ML book"],
            "Data Science": ["DataCamp", "Kaggle", "Python for Data Analysis book"]
        }
        
        skill_lower = skill.lower()
        for key, resources in resource_map.items():
            if key.lower() in skill_lower:
                return resources
        
        # Default resources
        return [
            f"Search for {skill} tutorials on YouTube",
            f"Check {skill} official documentation",
            f"Find {skill} courses on Coursera/edX"
        ]

# Test the real integration
if __name__ == "__main__":
    # Load curriculum data
    with open('giet_cse_skills.json', 'r') as f:
        curriculum_data = json.load(f)
    
    curriculum_skills = curriculum_data['overall_technical_skills']
    
    # Sample student skills
    student_skills = ["Python", "Java", "SQL", "Data Structures", "Algorithms"]
    
    # Initialize real integration system
    real_skill_twin = RealSkillTwinIntegration()
    
    # Analyze student for a target role with real market data
    target_role = "Software Developer"
    print(f"🔍 Analyzing {target_role} with real job market data...")
    
    analysis = real_skill_twin.comprehensive_real_analysis(
        student_skills, target_role, curriculum_skills
    )
    
    if "error" not in analysis:
        print(f"\n🎓 Real Skill-Twin Analysis for: {target_role}")
        print(f"Student skills: {analysis['student_profile']['total_skills']}")
        print(f"Jobs analyzed: {analysis['real_market_insights']['executive_summary']['total_jobs_analyzed']}")
        print(f"Market coverage: {analysis['real_market_insights']['executive_summary']['curriculum_coverage']}")
        print(f"Student-market match: {analysis['student_market_analysis']['overall_match_percentage']}%")
        
        print(f"\n🎯 Top Skills to Learn:")
        for rec in analysis['personalized_recommendations'][:5]:
            print(f"- {rec['skill']} ({rec['priority']} priority): {rec['estimated_time']}")
        
        # Save analysis
        with open('real_comprehensive_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n💾 Real analysis saved to real_comprehensive_analysis.json")
    else:
        print(f"❌ Analysis failed: {analysis['error']}")