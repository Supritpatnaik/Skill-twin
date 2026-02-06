"""
Real Job Scraper for Skill-Twin Engine
Scrapes actual job listings from LinkedIn, Naukri, and Indeed
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from typing import List, Dict, Optional
import logging
from urllib.parse import quote_plus, urljoin
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealJobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.rate_limit_delay = 3  # seconds between requests
        
    def setup_session(self):
        """Setup session with appropriate headers to avoid blocking"""
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
        time.sleep(self.rate_limit_delay + random.uniform(1.0, 3.0))
        
    def scrape_indeed_jobs(self, role: str, location: str = "India", limit: int = 15) -> List[Dict]:
        """Scrape real jobs from Indeed.com"""
        jobs = []
        try:
            # Indeed search URL
            encoded_role = quote_plus(role)
            encoded_location = quote_plus(location)
            search_url = f"https://in.indeed.com/jobs?q={encoded_role}&l={encoded_location}&from=searchOnHP"
            
            logger.info(f"Scraping Indeed: {search_url}")
            self.rate_limit()
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', {'data-jk': True})
            
            for card in job_cards[:limit]:
                try:
                    # Extract job details
                    job_key = card.get('data-jk')
                    if not job_key:
                        continue
                        
                    # Get job title
                    title_elem = card.find('h2', class_='jobTitle')
                    title = title_elem.get_text().strip() if title_elem else "N/A"
                    
                    # Get company name
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text().strip() if company_elem else "N/A"
                    
                    # Get location
                    location_elem = card.find('div', {'data-testid': 'job-location'})
                    location = location_elem.get_text().strip() if location_elem else location
                    
                    # Get salary (if available)
                    salary_elem = card.find('span', class_='estimated-salary')
                    salary = salary_elem.get_text().strip() if salary_elem else "Not specified"
                    
                    # Get job URL
                    job_url = f"https://in.indeed.com/viewjob?jk={job_key}"
                    
                    # Get detailed job description
                    description = self.get_indeed_job_description(job_url)
                    
                    # Extract experience requirement
                    experience = self.extract_experience_from_description(description)
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "url": job_url,
                        "posted_date": "Recent",  # Indeed doesn't show exact dates in search results
                        "source": "Indeed",
                        "salary": salary,
                        "experience_level": experience
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Indeed job card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
            
        return jobs
    
    def get_indeed_job_description(self, job_url: str) -> str:
        """Get detailed job description from Indeed job page"""
        try:
            self.rate_limit()
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors for job description
            description_selectors = [
                'div#jobDescriptionText',
                'div.jobsearch-jobDescriptionText',
                'div[itemprop="description"]'
            ]
            
            for selector in description_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    return desc_elem.get_text().strip()
            
            return "Detailed description not available"
            
        except Exception as e:
            logger.error(f"Error getting Indeed job description: {e}")
            return "Description not available"
    
    def scrape_naukri_jobs(self, role: str, location: str = "India", limit: int = 15) -> List[Dict]:
        """Scrape real jobs from Naukri.com"""
        jobs = []
        try:
            encoded_role = quote_plus(role)
            search_url = f"https://www.naukri.com/jobsvit-{encoded_role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
            
            logger.info(f"Scraping Naukri: {search_url}")
            self.rate_limit()
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_listings = soup.find_all('article', class_='jobTuple')
            
            for listing in job_listings[:limit]:
                try:
                    # Extract details
                    title_elem = listing.find('a', class_='title')
                    company_elem = listing.find('a', class_='subTitle')
                    location_elem = listing.find('li', class_='location')
                    exp_elem = listing.find('li', class_='experience')
                    salary_elem = listing.find('li', class_='salary')
                    
                    title = title_elem.get_text().strip() if title_elem else "N/A"
                    company = company_elem.get_text().strip() if company_elem else "N/A"
                    location = location_elem.get_text().strip() if location_elem else location
                    experience = exp_elem.get_text().strip() if exp_elem else "Not specified"
                    salary = salary_elem.get_text().strip() if salary_elem else "Not specified"
                    
                    # Get job URL
                    job_url = title_elem['href'] if title_elem and title_elem.get('href') else "N/A"
                    
                    # Get detailed description
                    description = self.get_naukri_job_description(job_url) if job_url != "N/A" else "Description not available"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "url": job_url,
                        "posted_date": "Recent",
                        "source": "Naukri",
                        "salary": salary,
                        "experience_level": experience
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Naukri listing: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Naukri: {e}")
            
        return jobs
    
    def get_naukri_job_description(self, job_url: str) -> str:
        """Get detailed job description from Naukri job page"""
        try:
            self.rate_limit()
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors
            description_selectors = [
                'div.datablock',
                'section.job-desc',
                'div.job-desc-main'
            ]
            
            for selector in description_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    return desc_elem.get_text().strip()
            
            return "Detailed description not available"
            
        except Exception as e:
            logger.error(f"Error getting Naukri job description: {e}")
            return "Description not available"
    
    def scrape_timesjobs_jobs(self, role: str, location: str = "India", limit: int = 15) -> List[Dict]:
        """Scrape real jobs from TimesJobs.com"""
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
                    location_elem = listing.find('ul', class_='top-jd-dtl clearfix')
                    exp_elem = listing.find('li', string=lambda text: text and ('yrs' in text.lower() or 'year' in text.lower()))
                    
                    title = title_elem.get_text().strip() if title_elem else "N/A"
                    company = company_elem.get_text().strip() if company_elem else "N/A"
                    location = location_elem.find('li').get_text().strip() if location_elem and location_elem.find('li') else location
                    experience = exp_elem.get_text().strip() if exp_elem else "Freshers welcome"
                    
                    # Get job URL
                    job_url = title_elem.find('a')['href'] if title_elem and title_elem.find('a') else "N/A"
                    
                    # Get detailed description
                    description = self.get_timesjobs_description(job_url) if job_url != "N/A" else "Description not available"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "url": job_url,
                        "posted_date": "Recent",
                        "source": "TimesJobs",
                        "salary": "Not specified",
                        "experience_level": experience
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing TimesJobs listing: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping TimesJobs: {e}")
            
        return jobs
    
    def get_timesjobs_description(self, job_url: str) -> str:
        """Get detailed job description from TimesJobs"""
        try:
            self.rate_limit()
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for job description
            desc_elem = soup.find('div', class_='jd-desc job-description-main')
            if desc_elem:
                return desc_elem.get_text().strip()
            
            # Alternative selectors
            alt_selectors = [
                'div.job-desc',
                'section.job-description',
                'div.description'
            ]
            
            for selector in alt_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    return desc_elem.get_text().strip()
            
            return "Detailed description not available"
            
        except Exception as e:
            logger.error(f"Error getting TimesJobs description: {e}")
            return "Description not available"
    
    def extract_skills_from_description(self, description: str) -> List[str]:
        """Extract technical skills from job description"""
        if not description or len(description) < 50:
            return []
        
        # Common technical skills keywords
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'linux', 'spring', 'django', 'flask',
            'tensorflow', 'pytorch', 'machine learning', 'data science', 'api',
            'rest', 'graphql', 'html', 'css', 'bootstrap', 'jquery', 'typescript',
            'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'php', 'ruby'
        ]
        
        found_skills = []
        description_lower = description.lower()
        
        for skill in tech_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, description_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def extract_experience_from_description(self, description: str) -> str:
        """Extract experience requirements from job description"""
        if not description:
            return "Not specified"
        
        # Look for experience patterns
        experience_patterns = [
            r'(\d+)\s*[-+]\s*(\d+)\s*years?',
            r'(\d+)\s*to\s*(\d+)\s*years?',
            r'(\d+)\s*\+?\s*years?',
            r'fresher',
            r'entry[-\s]?level',
            r'0[-\s]?1\s*year'
        ]
        
        description_lower = description.lower()
        
        for pattern in experience_patterns:
            match = re.search(pattern, description_lower)
            if match:
                if 'fresher' in description_lower or 'entry' in description_lower:
                    return "Freshers"
                elif '0-1' in description_lower or '0 1' in description_lower:
                    return "0-1 years"
                elif match.group(1):
                    if len(match.groups()) > 1 and match.group(2):
                        return f"{match.group(1)}-{match.group(2)} years"
                    else:
                        return f"{match.group(1)}+ years"
        
        return "Not specified"
    
    def aggregate_job_data(self, role: str, location: str = "India", limit: int = 20) -> Dict:
        """Aggregate job data from multiple sources"""
        all_jobs = []
        
        logger.info(f"Starting real job aggregation for: {role} in {location}")
        
        # Scrape from multiple sources
        sources = [
            ("Indeed", self.scrape_indeed_jobs),
            ("Naukri", self.scrape_naukri_jobs),
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
        
        # Extract skills from all job descriptions
        all_skills = []
        for job in all_jobs:
            skills = self.extract_skills_from_description(job['description'])
            all_skills.extend(skills)
            job['extracted_skills'] = skills
        
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
                "sources_used": len([job for job in all_jobs if job.get('source')]),
                "unique_companies": len(set(job['company'] for job in all_jobs if job['company'] != "N/A")),
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
                    "title": job['title'],
                    "company": job['company'],
                    "location": job['location'],
                    "description": job['description'][:500] + "..." if len(job['description']) > 500 else job['description'],
                    "url": job['url'],
                    "posted_date": job['posted_date'],
                    "source": job['source'],
                    "experience_level": job['experience_level'],
                    "salary": job['salary'],
                    "extracted_skills": job['extracted_skills']
                }
                for job in all_jobs
            ]
        }
        
        return result
    
    def analyze_experience_distribution(self, jobs: List[Dict]) -> Dict:
        """Analyze experience level distribution"""
        exp_count = {}
        for job in jobs:
            exp = job.get('experience_level', 'Not specified').lower()
            exp_count[exp] = exp_count.get(exp, 0) + 1
        return exp_count
    
    def analyze_location_distribution(self, jobs: List[Dict]) -> Dict:
        """Analyze location distribution"""
        loc_count = {}
        for job in jobs:
            loc = job.get('location', 'Not specified').split(',')[0].strip()
            loc_count[loc] = loc_count.get(loc, 0) + 1
        return dict(sorted(loc_count.items(), key=lambda x: x[1], reverse=True)[:10])

# Test the real scraper
if __name__ == "__main__":
    scraper = RealJobScraper()
    
    # Test with a common role
    role = "Software Developer"
    print(f"🔍 Scraping real jobs for: {role}")
    
    result = scraper.aggregate_job_data(role, "India", limit=15)
    
    print(f"\n📊 Job Market Analysis for: {role}")
    print(f"Total jobs found: {result['aggregation']['total_jobs_found']}")
    print(f"Sources used: {result['aggregation']['sources_used']}")
    print(f"Unique companies: {result['aggregation']['unique_companies']}")
    print(f"\nTop skills in demand:")
    for i, skill in enumerate(result['market_insights']['top_skills'][:10], 1):
        count = result['market_insights']['skill_frequency'][skill.lower()]
        print(f"{i}. {skill} ({count} mentions)")
    
    # Save results
    with open(f"real_{role.replace(' ', '_')}_market_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to real_{role.replace(' ', '_')}_market_analysis.json")