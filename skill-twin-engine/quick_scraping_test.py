"""
Quick test for real job scraping
"""

import requests
from bs4 import BeautifulSoup
import time

def quick_test():
    print("🚀 Quick Real Job Scraping Test")
    print("=" * 40)
    
    # Test Indeed
    print("1. Testing Indeed scraping...")
    try:
        url = "https://in.indeed.com/jobs?q=Software+Developer&l=India"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = soup.find_all('div', {'data-jk': True})
            print(f"   Found {len(jobs)} job cards")
            
            if jobs:
                first_job = jobs[0]
                title_elem = first_job.find('h2', class_='jobTitle')
                company_elem = first_job.find('span', class_='companyName')
                
                title = title_elem.get_text().strip() if title_elem else "No title"
                company = company_elem.get_text().strip() if company_elem else "No company"
                
                print(f"   Sample: {title} at {company}")
                print("   ✅ Indeed scraping working!")
            else:
                print("   ⚠️ No jobs found in response")
        else:
            print(f"   ❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test Naukri
    print("\n2. Testing Naukri scraping...")
    try:
        url = "https://www.naukri.com/jobsvit-software-developer-jobs-in-india"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = soup.find_all('article', class_='jobTuple')
            print(f"   Found {len(jobs)} job listings")
            
            if jobs:
                first_job = jobs[0]
                title_elem = first_job.find('a', class_='title')
                company_elem = first_job.find('a', class_='subTitle')
                
                title = title_elem.get_text().strip() if title_elem else "No title"
                company = company_elem.get_text().strip() if company_elem else "No company"
                
                print(f"   Sample: {title} at {company}")
                print("   ✅ Naukri scraping working!")
            else:
                print("   ⚠️ No jobs found in response")
        else:
            print(f"   ❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Test Complete!")

if __name__ == "__main__":
    quick_test()