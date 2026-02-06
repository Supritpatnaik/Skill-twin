"""
Real Job Market Skill-Twin Engine
Streamlit app with real web scraping functionality
"""

import streamlit as st
import json
import time
from typing import List
from real_job_integration import RealSkillTwinIntegration

def main():
    st.set_page_config(
        page_title="Real Skill-Twin Engine", 
        page_icon="🎓", 
        layout="wide"
    )
    
    st.title("🎓 Real Skill-Twin Engine")
    st.markdown("Real-time job market analysis with actual web scraping")
    
    # Initialize real analyzer
    @st.cache_resource
    def get_analyzer():
        return RealSkillTwinIntegration()
    
    analyzer = get_analyzer()
    
    # Load curriculum data
    try:
        with open('giet_cse_skills.json', 'r') as f:
            curriculum_data = json.load(f)
        curriculum_skills = curriculum_data['overall_technical_skills']
    except FileNotFoundError:
        st.error("Curriculum data file not found!")
        curriculum_skills = []
    
    # 1. User Information
    st.subheader("👤 Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
    with col2:
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "ME", "CE", "Other"])
    
    year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th"])
    
    # 2. Skills Input
    st.subheader("🛠️ Your Technical Skills")
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
        st.warning("Please enter your skills to proceed")
    
    # 3. Job Role Selection
    st.subheader("🎯 Target Job Role")
    common_roles = [
        "Software Developer",
        "Full Stack Developer", 
        "Data Scientist",
        "Machine Learning Engineer",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Python Developer",
        "Java Developer",
        "Data Analyst"
    ]
    
    role = st.selectbox("Choose your target role", common_roles)
    
    # 4. Location Preference
    st.subheader("📍 Location Preference")
    location = st.selectbox(
        "Job Location", 
        ["India", "Bangalore", "Hyderabad", "Pune", "Chennai", "Delhi", "Mumbai"]
    )
    
    # 5. Real Job Market Analysis
    st.subheader("🔍 Real Job Market Analysis")
    
    if st.button("📊 Fetch Real Job Market Data", type="primary"):
        if not student_skills:
            st.error("Please enter your skills first!")
            return
            
        with st.spinner("🔍 Scraping real job portals... This may take 1-2 minutes"):
            try:
                # Perform real analysis
                analysis = analyzer.comprehensive_real_analysis(
                    student_skills, role, curriculum_skills, location
                )
                
                if "error" in analysis:
                    st.error(f"❌ Analysis failed: {analysis['error']}")
                else:
                    # Store results in session state
                    st.session_state.real_analysis = analysis
                    st.success("✅ Real job market analysis complete!")
                    
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
    
    # 6. Display Results
    if 'real_analysis' in st.session_state:
        results = st.session_state.real_analysis
        
        # Summary Dashboard
        st.subheader(f"🎯 Analysis Results for {role}")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Your Skills", 
                results['student_profile']['total_skills']
            )
        with col2:
            st.metric(
                "Market Match", 
                f"{results['student_market_analysis']['overall_match_percentage']}%"
            )
        with col3:
            st.metric(
                "Skills to Learn", 
                results['student_market_analysis']['gaps_identified']
            )
        with col4:
            jobs_analyzed = results['real_market_insights']['executive_summary']['total_jobs_analyzed']
            st.metric("Jobs Analyzed", jobs_analyzed)
        
        # Detailed Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Market Insights", 
            "Your Gaps", 
            "Learning Plan", 
            "Curriculum Analysis", 
            "Raw Data"
        ])
        
        with tab1:
            summary = results['real_market_insights']['executive_summary']
            
            st.write(f"**📊 Market Overview:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• **Jobs Analyzed:** {summary['total_jobs_analyzed']}")
                st.write(f"• **Sources Used:** {summary['sources_used']}")
                st.write(f"• **Location:** {summary['location']}")
            with col2:
                st.write(f"• **Total Market Skills:** {summary['total_market_skills']}")
                st.write(f"• **Skills Covered:** {summary['skills_covered']}")
                st.write(f"• **Skills Missing:** {summary['skills_missing']}")
            
            st.write("**🔥 Top Market Skills (Real Data):**")
            skill_data = results['real_market_insights']['market_skills']
            for i, skill in enumerate(skill_data['top_skills'][:15], 1):
                frequency = skill_data['skill_frequency'].get(skill, 0)
                st.write(f"{i}. **{skill}** ({frequency} job postings)")
        
        with tab2:
            gaps = results['student_market_analysis']['top_gaps']
            if gaps:
                st.write("**⚠️ Skills you need to develop:**")
                for gap in gaps[:12]:
                    urgency_color = "🔴" if gap['urgency'] == "High" else "🟡"
                    st.write(f"{urgency_color} **{gap['skill']}** (Match: {gap['match_score']}, Urgency: {gap['urgency']})")
            else:
                st.success("🎉 Excellent! Your skills align well with market demands.")
        
        with tab3:
            st.write("**📚 Personalized Learning Plan (Based on Real Market Data):**")
            recommendations = results['personalized_recommendations']
            
            for i, rec in enumerate(recommendations[:10], 1):
                priority_emoji = "🔴" if rec['priority'] == "High" else "🟡" if rec['priority'] == "Medium" else "🟢"
                
                with st.expander(f"{priority_emoji} {i}. {rec['skill']} ({rec['priority']} priority)"):
                    st.write(f"**Type:** {rec['type']}")
                    st.write(f"**Time needed:** {rec['estimated_time']}")
                    st.write(f"**Market demand:** {rec['market_demand']}")
                    st.write(f"**Impact:** {rec['impact']}")
                    st.write(f"**Learning resources:**")
                    for resource in rec['resources'][:3]:
                        st.write(f"• {resource}")
        
        with tab4:
            st.write("**🏛️ University Curriculum Analysis:**")
            
            exec_summary = results['real_market_insights']['executive_summary']
            st.metric("Curriculum Coverage", exec_summary['curriculum_coverage'])
            
            gap_analysis = results['real_market_insights']['gap_analysis']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Well Covered", exec_summary['skills_covered'])
            with col2:
                st.metric("Partially Covered", exec_summary['skills_partially_covered'])
            with col3:
                st.metric("Not Covered", exec_summary['skills_missing'])
            
            st.write("**📋 Curriculum Recommendations:**")
            recommendations = results['real_market_insights']['recommendations']
            for rec in recommendations[:8]:
                priority_emoji = "🔴" if rec['priority'] == "High" else "🟡"
                st.write(f"{priority_emoji} **{rec['skill']}** - {rec['suggested_action']}")
        
        with tab5:
            st.write("**📋 Raw Job Market Data:**")
            if st.checkbox("Show detailed job listings"):
                raw_data = results['real_market_insights']['raw_job_data']
                jobs = raw_data['jobs'][:10]  # Show first 10 jobs
                
                for i, job in enumerate(jobs, 1):
                    with st.expander(f"{i}. {job['title']} at {job['company']}"):
                        st.write(f"**Company:** {job['company']}")
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Source:** {job['source']}")
                        st.write(f"**Experience:** {job['experience_level']}")
                        st.write(f"**Extracted Skills:** {', '.join(job['extracted_skills'][:10])}")
                        st.write(f"**Job URL:** [View Job]({job['url']})")
            
            if st.checkbox("Show complete JSON data"):
                st.json(results)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        <p><strong>Real Skill-Twin Engine</strong> - Bridging the gap between education and industry</p>
        <p>Real-time job market data scraped from Indeed, Naukri, and TimesJobs</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()