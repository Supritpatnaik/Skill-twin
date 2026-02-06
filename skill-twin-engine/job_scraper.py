"""
Job Scraper Module for Skill-Twin Engine
Scrapes live job descriptions from LinkedIn, Naukri.com, and other job portals
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class JobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)
        
    def scrape_linkedin_jobs(self, role: str, location: str = "India", limit: int = 10) -> List[Dict]:
        """
        Scrape job listings from LinkedIn (simplified version - would need LinkedIn API for full functionality)
        Note: LinkedIn's terms prohibit scraping, so this is a placeholder for demonstration
        """
        jobs = []
        try:
            # This is a simplified approach - real LinkedIn scraping would require API or proper authentication
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}"
            
            # In a real implementation, you'd need to:
            # 1. Handle authentication
            # 2. Use LinkedIn Jobs API (requires partnership)
            # 3. Implement proper rate limiting
            
            # For demonstration, I'll create sample data
            sample_jobs = [
                {
                    "title": f"{role} - Fresher",
                    "company": "Tech Solutions Pvt Ltd",
                    "location": "Bangalore, India",
                    "description": "Looking for fresh graduates in Computer Science with knowledge of Python, SQL, and web development. Good problem-solving skills required.",
                    "url": "https://linkedin.com/jobs/sample1",
                    "posted_date": "2026-02-01"
                },
                {
                    "title": f"Junior {role}",
                    "company": "Digital Innovations",
                    "location": "Hyderabad, India", 
                    "description": "Entry-level position for recent graduates. Required skills: Java, Spring Boot, REST APIs, MySQL. Freshers welcome with good academic background.",
                    "url": "https://linkedin.com/jobs/sample2",
                    "posted_date": "2026-01-28"
                }
            ]
            
            jobs.extend(sample_jobs[:limit])
            print(f"⚠️ LinkedIn scraping requires proper API access. Returning {len(jobs)} sample jobs for demonstration.")
            
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            
        return jobs
    
    def scrape_naukri_jobs(self, role: str, location: str = "India", limit: int = 10) -> List[Dict]:
        """
        Scrape job listings from Naukri.com
        """
        jobs = []
        try:
            # Naukri search URL format
            search_url = f"https://www.naukri.com/jobsvit-{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings (selectors may need updating based on current Naukri HTML structure)
            job_elements = soup.find_all('article', class_='jobTuple bgWhite br4 mb-8')
            
            for job_element in job_elements[:limit]:
                try:
                    # Extract job details
                    title_elem = job_element.find('a', class_='title')
                    company_elem = job_element.find('a', class_='subTitle')
                    location_elem = job_element.find('li', class_='location')
                    desc_elem = job_element.find('div', class_='jobDescriptionText')
                    exp_elem = job_element.find('li', class_='experience')
                    
                    job = {
                        "title": title_elem.text.strip() if title_elem else "N/A",
                        "company": company_elem.text.strip() if company_elem else "N/A",
                        "location": location_elem.text.strip() if location_elem else "N/A",
                        "description": desc_elem.text.strip() if desc_elem else "N/A",
                        "experience": exp_elem.text.strip() if exp_elem else "Freshers",
                        "url": title_elem['href'] if title_elem and title_elem.get('href') else "N/A",
                        "posted_date": "2026-02-05",  # Placeholder
                        "source": "Naukri.com"
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"Error parsing job element: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping Naukri: {e}")
            
        return jobs
    
    def extract_skills_from_description(self, job_description: str) -> List[str]:
        """
        Extract skills from job description using OpenAI
        """
        if not job_description or len(job_description.strip()) < 50:
            return []
            
        try:
            prompt = f"""
            Extract technical skills, programming languages, tools, and technologies from this job description.
            Return ONLY a JSON array of strings. Exclude soft skills unless they are technical.
            
            Job Description: {job_description[:2000]}
            
            Output format: ["Python", "JavaScript", "React", "AWS"]
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result if isinstance(result, list) else []
            
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return []
    
    def get_job_skills_for_role(self, role: str, location: str = "India", limit: int = 5) -> Dict:
        """
        Get comprehensive job skills for a specific role by scraping multiple sources
        """
        all_jobs = []
        all_skills = []
        
        # Scrape from different sources
        print(f"🔍 Scraping jobs for role: {role} in {location}")
        
        # LinkedIn jobs
        linkedin_jobs = self.scrape_linkedin_jobs(role, location, limit//2)
        all_jobs.extend(linkedin_jobs)
        
        # Naukri jobs  
        naukri_jobs = self.scrape_naukri_jobs(role, location, limit//2)
        all_jobs.extend(naukri_jobs)
        
        # Extract skills from all job descriptions
        print(f"📊 Analyzing {len(all_jobs)} job descriptions for skills...")
        for job in all_jobs:
            skills = self.extract_skills_from_description(job['description'])
            all_skills.extend(skills)
            job['extracted_skills'] = skills
        
        # Remove duplicates and count frequency
        skill_frequency = {}
        for skill in all_skills:
            skill_lower = skill.lower().strip()
            if skill_lower:
                skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
        
        # Sort by frequency and return top skills
        sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
        top_skills = [skill.title() for skill, count in sorted_skills[:20]]
        
        return {
            "role": role,
            "total_jobs_analyzed": len(all_jobs),
            "top_skills": top_skills,
            "skill_frequency": dict(sorted_skills[:20]),
            "jobs": all_jobs,
            "extraction_summary": {
                "total_skills_extracted": len(all_skills),
                "unique_skills": len(skill_frequency),
                "average_skills_per_job": len(all_skills) / len(all_jobs) if all_jobs else 0
            }
        }
    
    def save_job_data(self, job_data: Dict, filename: str = None):
        """
        Save scraped job data to JSON file
        """
        if not filename:
            filename = f"job_data_{int(time.time())}.json"
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Job data saved to {filename}")

# Example usage
if __name__ == "__main__":
    scraper = JobScraper()
    
    # Test with a common role
    role = "Software Developer"
    job_skills = scraper.get_job_skills_for_role(role, "India", limit=5)
    
    print(f"\n🎯 Job Market Analysis for: {role}")
    print(f"Total jobs analyzed: {job_skills['total_jobs_analyzed']}")
    print(f"Top skills required: {', '.join(job_skills['top_skills'][:10])}")
    print(f"Unique skills identified: {job_skills['extraction_summary']['unique_skills']}")
    
    # Save the data
    scraper.save_job_data(job_skills, f"{role.replace(' ', '_')}_market_analysis.json")