"""
Advanced Job Scraper with Multiple Sources and Rate Limiting
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobListing:
    title: str
    company: str
    location: str
    description: str
    url: str
    posted_date: str
    source: str
    experience_level: str = "Not specified"
    salary: str = "Not specified"
    skills: List[str] = None

class AdvancedJobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.rate_limit_delay = 2  # seconds between requests
        
    def setup_session(self):
        """Setup session with appropriate headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(headers)
        
    def rate_limit(self):
        """Implement rate limiting to avoid being blocked"""
        time.sleep(self.rate_limit_delay + random.uniform(0.5, 2.0))
        
    def scrape_indeed_jobs(self, role: str, location: str = "India", limit: int = 10) -> List[JobListing]:
        """Scrape jobs from Indeed.com"""
        jobs = []
        try:
            # Indeed search URL
            encoded_role = quote_plus(role)
            encoded_location = quote_plus(location)
            search_url = f"https://in.indeed.com/jobs?q={encoded_role}&l={encoded_location}"
            
            logger.info(f"Scraping Indeed: {search_url}")
            self.rate_limit()
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards (selectors may need updating)
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:limit]:
                try:
                    # Extract job details
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', {'data-testid': 'job-location'})
                    salary_elem = card.find('span', class_='estimated-salary')
                    date_elem = card.find('span', class_='date')
                    
                    # Get job description from the job page
                    if title_elem and title_elem.find('a'):
                        job_url = "https://in.indeed.com" + title_elem.find('a')['href']
                        description = self.get_job_description(job_url)
                    else:
                        description = "Description not available"
                        job_url = "N/A"
                    
                    job = JobListing(
                        title=title_elem.get_text().strip() if title_elem else "N/A",
                        company=company_elem.get_text().strip() if company_elem else "N/A",
                        location=location_elem.get_text().strip() if location_elem else location,
                        description=description,
                        url=job_url,
                        posted_date=date_elem.get_text().strip() if date_elem else "N/A",
                        source="Indeed",
                        salary=salary_elem.get_text().strip() if salary_elem else "Not specified",
                        experience_level="Entry level" if title_elem and "fresher" in title_elem.get_text().lower() else "Not specified"
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Indeed job card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
            
        return jobs
    
    def scrape_timesjobs_jobs(self, role: str, location: str = "India", limit: int = 10) -> List[JobListing]:
        """Scrape jobs from TimesJobs.com"""
        jobs = []
        try:
            encoded_role = quote_plus(role)
            search_url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={encoded_role}&txtLocation={location}"
            
            logger.info(f"Scraping TimesJobs: {search_url}")
            self.rate_limit()
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_listings = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
            
            for listing in job_listings[:limit]:
                try:
                    # Extract details
                    title_elem = listing.find('h2')
                    company_elem = listing.find('h3', class_='joblist-comp-name')
                    location_elem = listing.find('ul', class_='top-jd-dtl clearfix').find('li') if listing.find('ul', class_='top-jd-dtl clearfix') else None
                    exp_elem = listing.find('li', string=lambda text: text and 'yrs' in text.lower()) if listing.find('ul', class_='top-jd-dtl clearfix') else None
                    desc_elem = listing.find('ul', class_='list-job-dtl clearfix')
                    
                    # Get detailed job page
                    if title_elem and title_elem.find('a'):
                        job_url = title_elem.find('a')['href']
                        description = self.get_job_description(job_url)
                    else:
                        description = desc_elem.get_text().strip() if desc_elem else "Description not available"
                        job_url = "N/A"
                    
                    job = JobListing(
                        title=title_elem.get_text().strip() if title_elem else "N/A",
                        company=company_elem.get_text().strip() if company_elem else "N/A",
                        location=location_elem.get_text().strip() if location_elem else location,
                        description=description,
                        url=job_url,
                        posted_date="N/A",  # TimesJobs doesn't clearly show dates
                        source="TimesJobs",
                        experience_level=exp_elem.get_text().strip() if exp_elem else "Freshers welcome",
                        skills=self.extract_skills_from_text(description)
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing TimesJobs listing: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping TimesJobs: {e}")
            
        return jobs
    
    def get_job_description(self, job_url: str) -> str:
        """Get detailed job description from job page"""
        try:
            self.rate_limit()
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors for job description
            description_selectors = [
                'div.jobDescriptionText',
                'div.job-desc',
                'div.description',
                'div.job-posting-description',
                'div[itemprop="description"]'
            ]
            
            for selector in description_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    return desc_elem.get_text().strip()
            
            return "Detailed description not available"
            
        except Exception as e:
            logger.error(f"Error getting job description: {e}")
            return "Description not available"
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching"""
        if not text:
            return []
            
        # Common technical skills keywords
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'linux', 'spring', 'django', 'flask',
            'tensorflow', 'pytorch', 'machine learning', 'data science', 'api',
            'rest', 'graphql', 'html', 'css', 'bootstrap', 'jquery', 'typescript'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in tech_skills:
            if skill.lower() in text_lower:
                # Find the original case from the text
                start_idx = text_lower.find(skill.lower())
                if start_idx != -1:
                    original_skill = text[start_idx:start_idx + len(skill)]
                    found_skills.append(original_skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def aggregate_job_data(self, role: str, location: str = "India", limit: int = 15) -> Dict:
        """Aggregate job data from multiple sources"""
        all_jobs = []
        
        logger.info(f"Starting job aggregation for: {role} in {location}")
        
        # Scrape from multiple sources
        sources = [
            ("Indeed", self.scrape_indeed_jobs),
            ("TimesJobs", self.scrape_timesjobs_jobs)
        ]
        
        for source_name, scraper_func in sources:
            try:
                logger.info(f"Scraping {source_name}...")
                jobs = scraper_func(role, location, limit//len(sources))
                all_jobs.extend(jobs)
                logger.info(f"Found {len(jobs)} jobs from {source_name}")
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {e}")
                continue
        
        # Extract and aggregate skills
        all_skills = []
        for job in all_jobs:
            if job.skills is None:
                job.skills = self.extract_skills_from_text(job.description)
            all_skills.extend(job.skills)
        
        # Count skill frequency
        skill_count = {}
        for skill in all_skills:
            skill_lower = skill.lower()
            skill_count[skill_lower] = skill_count.get(skill_lower, 0) + 1
        
        # Sort by frequency
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        top_skills = [skill.title() for skill, count in sorted_skills[:25]]
        
        # Prepare result
        result = {
            "search_query": {
                "role": role,
                "location": location,
                "limit": limit
            },
            "aggregation": {
                "total_jobs_found": len(all_jobs),
                "sources_used": len([job for job in all_jobs if job.source]),
                "unique_companies": len(set(job.company for job in all_jobs if job.company != "N/A")),
                "date_range": "Last 30 days"
            },
            "market_insights": {
                "top_skills": top_skills,
                "skill_frequency": dict(sorted_skills[:25]),
                "experience_distribution": self.analyze_experience_distribution(all_jobs),
                "location_distribution": self.analyze_location_distribution(all_jobs)
            },
            "jobs": [
                {
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description[:500] + "..." if len(job.description) > 500 else job.description,
                    "url": job.url,
                    "posted_date": job.posted_date,
                    "source": job.source,
                    "experience_level": job.experience_level,
                    "salary": job.salary,
                    "extracted_skills": job.skills
                }
                for job in all_jobs
            ]
        }
        
        return result
    
    def analyze_experience_distribution(self, jobs: List[JobListing]) -> Dict:
        """Analyze experience level distribution"""
        exp_count = {}
        for job in jobs:
            exp = job.experience_level.lower()
            exp_count[exp] = exp_count.get(exp, 0) + 1
        return exp_count
    
    def analyze_location_distribution(self, jobs: List[JobListing]) -> Dict:
        """Analyze location distribution"""
        loc_count = {}
        for job in jobs:
            loc = job.location.split(',')[0].strip()  # Get city name
            loc_count[loc] = loc_count.get(loc, 0) + 1
        return dict(sorted(loc_count.items(), key=lambda x: x[1], reverse=True)[:10])

# Example usage
if __name__ == "__main__":
    scraper = AdvancedJobScraper()
    
    # Test with a common role
    role = "Full Stack Developer"
    result = scraper.aggregate_job_data(role, "India", limit=20)
    
    print(f"\n📊 Job Market Analysis for: {role}")
    print(f"Total jobs found: {result['aggregation']['total_jobs_found']}")
    print(f"Sources used: {result['aggregation']['sources_used']}")
    print(f"Unique companies: {result['aggregation']['unique_companies']}")
    print(f"\nTop skills in demand:")
    for i, skill in enumerate(result['market_insights']['top_skills'][:10], 1):
        count = result['market_insights']['skill_frequency'][skill.lower()]
        print(f"{i}. {skill} ({count} mentions)")
    
    # Save results
    with open(f"{role.replace(' ', '_')}_market_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to {role.replace(' ', '_')}_market_analysis.json")