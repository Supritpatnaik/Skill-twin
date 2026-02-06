"""
Test script for job scraping functionality
"""

import json
from job_scraper import JobScraper
from advanced_job_scraper import AdvancedJobScraper
from job_market_integration import IntegratedSkillTwin

def test_basic_job_scraper():
    """Test basic job scraper functionality"""
    print("🧪 Testing Basic Job Scraper...")
    scraper = JobScraper()
    
    # Test skill extraction
    sample_description = """
    We are looking for a Software Developer with experience in Python, JavaScript, and React.
    Must have knowledge of SQL databases and REST APIs. 
    Experience with AWS and Docker is preferred.
    """
    
    skills = scraper.extract_skills_from_description(sample_description)
    print(f"Extracted skills: {skills}")
    
    # Test job skills for role
    job_skills = scraper.get_job_skills_for_role("Software Developer", "India", limit=3)
    print(f"Job skills for Software Developer: {job_skills['top_skills'][:10]}")
    
    return True

def test_advanced_job_scraper():
    """Test advanced job scraper functionality"""
    print("\n🧪 Testing Advanced Job Scraper...")
    scraper = AdvancedJobScraper()
    
    # Test skill extraction from text
    text = "Looking for candidates with Python, Machine Learning, and Data Science skills"
    skills = scraper.extract_skills_from_text(text)
    print(f"Extracted skills from text: {skills}")
    
    return True

def test_integration():
    """Test full integration"""
    print("\n🧪 Testing Full Integration...")
    
    # Load curriculum data
    try:
        with open('giet_cse_skills.json', 'r') as f:
            curriculum_data = json.load(f)
        curriculum_skills = curriculum_data['overall_technical_skills']
        print(f"Loaded {len(curriculum_skills)} curriculum skills")
        
        # Test integrated analysis
        skill_twin = IntegratedSkillTwin()
        student_skills = ["Python", "Java", "SQL", "Data Structures"]
        
        analysis = skill_twin.analyze_student_with_market_data(
            student_skills, "Software Developer", curriculum_skills
        )
        
        if "error" not in analysis:
            print("✅ Integration test passed!")
            print(f"Student match: {analysis['student_market_match']['overall_match_percentage']}%")
            print(f"Skills missing: {len(analysis['student_market_match']['top_gaps'])}")
        else:
            print(f"❌ Integration test failed: {analysis['error']}")
            
        return "error" not in analysis
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Job Scraping Tests\n")
    
    tests = [
        ("Basic Job Scraper", test_basic_job_scraper),
        ("Advanced Job Scraper", test_advanced_job_scraper),
        ("Full Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Job scraping functionality is ready.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()