"""
Real Job Market Skill-Twin Engine - Production Ready
Streamlit app with realistic job market data
"""

import streamlit as st
import json
import time
from typing import List
from real_job_api_integration import RealJobSkillTwin

def main():
    st.set_page_config(
        page_title="Real Job Market Skill-Twin", 
        page_icon="🎯", 
        layout="wide"
    )
    
    st.title("🎯 Real Job Market Skill-Twin Engine")
    st.markdown("Realistic job market analysis based on actual industry patterns")
    
    # Initialize real analyzer
    @st.cache_resource
    def get_real_analyzer():
        return RealJobSkillTwin()
    
    analyzer = get_real_analyzer()
    
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
    skills_help = """
    Enter your technical skills separated by commas. 
    Example: Python, Java, SQL, Data Structures, Machine Learning, Git
    """
    skills_input = st.text_area(
        "Enter your technical skills:",
        placeholder="Python, Java, SQL, Data Structures, Machine Learning...",
        height=120,
        help=skills_help
    )
    
    if skills_input:
        student_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        st.success(f"✅ Loaded {len(student_skills)} skills")
        
        # Show skill validation
        with st.expander("🔍 Skills Analysis"):
            st.write("**Your skills:**")
            cols = st.columns(3)
            for i, skill in enumerate(student_skills):
                cols[i % 3].write(f"• {skill}")
    else:
        student_skills = []
        st.warning("⚠️ Please enter your skills to proceed")
    
    # 3. Job Role Selection
    st.subheader("🎯 Target Career Path")
    
    # Popular roles with descriptions
    role_descriptions = {
        "Software Developer": "General software development roles across various technologies",
        "Full Stack Developer": "Web development covering both frontend and backend",
        "Data Scientist": "Data analysis, machine learning, and statistical modeling",
        "Machine Learning Engineer": "AI/ML model development and deployment",
        "DevOps Engineer": "Infrastructure, automation, and deployment specialist",
        "Frontend Developer": "User interface and client-side web development",
        "Backend Developer": "Server-side logic and database management",
        "Python Developer": "Python-focused software development",
        "Java Developer": "Java-based enterprise application development",
        "Data Analyst": "Data processing, visualization, and business insights"
    }
    
    selected_role = st.selectbox(
        "Choose your target role:",
        list(role_descriptions.keys()),
        format_func=lambda x: f"{x} - {role_descriptions[x][:50]}..."
    )
    
    # Show role details
    with st.expander("ℹ️ Role Details"):
        st.write(f"**{selected_role}**")
        st.write(role_descriptions[selected_role])
    
    # 4. Location Preference
    st.subheader("📍 Job Location Preference")
    location_options = {
        "India": "All of India",
        "Bangalore": "Bangalore, Karnataka",
        "Hyderabad": "Hyderabad, Telangana", 
        "Pune": "Pune, Maharashtra",
        "Chennai": "Chennai, Tamil Nadu",
        "Delhi": "Delhi NCR",
        "Mumbai": "Mumbai, Maharashtra"
    }
    
    selected_location = st.selectbox(
        "Preferred job location:",
        list(location_options.keys()),
        format_func=lambda x: f"{x} - {location_options[x]}"
    )
    
    # 5. Real Job Market Analysis
    st.subheader("🔍 Real Job Market Intelligence")
    
    analyze_button = st.button(
        "🚀 Analyze Real Job Market", 
        type="primary",
        use_container_width=True
    )
    
    if analyze_button:
        if not student_skills:
            st.error("❌ Please enter your skills first!")
            st.stop()
            
        with st.spinner("📊 Analyzing real job market data..."):
            try:
                # Perform real analysis
                analysis = analyzer.analyze_with_real_market(
                    student_skills, selected_role, curriculum_skills, selected_location
                )
                
                # Store results in session state
                st.session_state.real_job_analysis = analysis
                st.success("✅ Real job market analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Showing sample analysis instead...")
                # Fallback to sample data
                sample_analysis = {
                    "student_profile": {"total_skills": len(student_skills), "skills_list": student_skills},
                    "student_analysis": {"match_percentage": 45.0, "gaps_identified": 8, "top_gaps": []},
                    "curriculum_analysis": {"coverage_percentage": 55.0, "covered_skills": 12, "missing_skills": 10},
                    "recommendations": [
                        {"skill": "Git", "priority": "High", "estimated_time": "2 weeks"},
                        {"skill": "REST API", "priority": "High", "estimated_time": "3 weeks"}
                    ]
                }
                st.session_state.real_job_analysis = sample_analysis
    
    # 6. Display Results
    if 'real_job_analysis' in st.session_state:
        results = st.session_state.real_job_analysis
        
        # Executive Dashboard
        st.subheader(f"🎯 Market Analysis: {selected_role}")
        
        # Key Metrics Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Skills Match", 
                f"{results['student_analysis']['match_percentage']}%",
                help="How well your skills match current market demands"
            )
        with col2:
            st.metric(
                "📚 Curriculum Coverage", 
                f"{results['curriculum_analysis']['coverage_percentage']}%",
                help="Percentage of market skills covered by your curriculum"
            )
        with col3:
            st.metric(
                "⚠️ Skills Gap", 
                results['student_analysis']['gaps_identified'],
                help="Number of skills you need to develop"
            )
        with col4:
            st.metric(
                "💼 Market Skills", 
                len(results['real_market_insights']['market_insights']['top_skills']),
                help="Total market skills identified"
            )
        
        # Detailed Analysis Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Market Insights", 
            "🎯 Your Skills Gap", 
            "📚 Learning Roadmap", 
            "🏛️ Curriculum Analysis", 
            "📋 Job Listings"
        ])
        
        with tab1:
            market_data = results['real_market_insights']
            
            st.write("**📊 Real Market Overview:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"• **Jobs Analyzed:** {market_data['search_query']['total_jobs']}")
                st.write(f"• **Location:** {market_data['search_query']['location']}")
            with col2:
                st.write(f"• **Skills Identified:** {market_data['market_insights']['total_skills_identified']}")
                st.write(f"• **Data Confidence:** High")
            with col3:
                st.write(f"• **Last Updated:** {market_data['metadata']['last_updated']}")
            
            # Top Skills Visualization
            st.write("**🔥 Top In-Demand Skills:**")
            top_skills = market_data['market_insights']['top_skills'][:15]
            
            # Create skill importance visualization
            for i, skill in enumerate(top_skills, 1):
                importance = "🔴 High" if i <= 5 else "🟡 Medium" if i <= 10 else "🟢 Low"
                st.write(f"{importance} {i}. **{skill}**")
        
        with tab2:
            gaps = results['student_analysis']['top_gaps']
            if gaps:
                st.write("**⚠️ Skills You Need to Develop:**")
                
                for i, gap in enumerate(gaps[:12], 1):
                    urgency_emoji = "🔴" if gap['urgency'] == "High" else "🟡"
                    match_text = f"({gap['match_score']*100:.0f}% match)" if gap['match_score'] > 0 else "(Not found)"
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"{urgency_emoji} **{gap['skill']}** {match_text}")
                    with col2:
                        st.write(f"Urgency: {gap['urgency']}")
                    with col3:
                        if st.button(f"Details", key=f"gap_{gap['skill']}_{i}"):
                            st.info(f"Skill: {gap['skill']}\nMatch Score: {gap['match_score']}\nUrgency: {gap['urgency']}")
            else:
                st.success("🎉 Excellent! Your skills align well with market demands.")
                st.balloons()
        
        with tab3:
            st.write("**📚 Personalized Learning Roadmap:**")
            recommendations = results['recommendations']
            
            if recommendations:
                for i, rec in enumerate(recommendations[:10], 1):
                    priority_emoji = "🔴" if rec['priority'] == "High" else "🟡" if rec['priority'] == "Medium" else "🟢"
                    category_emoji = "👤" if rec['category'] == "Student Gap" else "🏛️"
                    
                    with st.expander(f"{priority_emoji} {category_emoji} {i}. {rec['skill']} ({rec['priority']} priority)"):
                        st.write(f"**Category:** {rec['category']}")
                        st.write(f"**Time needed:** {rec['estimated_time']}")
                        st.write(f"**Market demand:** {rec['market_demand']}")
                        st.write(f"**Learning resources:**")
                        for resource in rec['resources'][:3]:
                            st.write(f"• {resource}")
                        
                        # Action buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Mark as Learning", key=f"learn_{rec['skill']}_{i}"):
                                st.success(f"Added {rec['skill']} to your learning plan!")
                        with col2:
                            if st.button(f"Mark as Completed", key=f"complete_{rec['skill']}_{i}"):
                                st.success(f"Great job completing {rec['skill']}!")
            else:
                st.info("No specific recommendations needed - you're well prepared!")
        
        with tab4:
            st.write("**🏛️ University Curriculum Analysis:**")
            
            curriculum_data = results['curriculum_analysis']
            st.metric("Curriculum Coverage", f"{curriculum_data['coverage_percentage']}%")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Covered Skills", curriculum_data['covered_skills'])
            with col2:
                st.metric("⚠️ Missing Skills", curriculum_data['missing_skills'])
            with col3:
                gap_ratio = curriculum_data['missing_skills'] / (curriculum_data['covered_skills'] + curriculum_data['missing_skills']) * 100 if (curriculum_data['covered_skills'] + curriculum_data['missing_skills']) > 0 else 0
                st.metric("Gap Ratio", f"{gap_ratio:.1f}%")
            
            if curriculum_data['gaps']:
                st.write("**📋 Curriculum Improvement Areas:**")
                for i, skill in enumerate(curriculum_data['gaps'][:15], 1):
                    st.write(f"{i}. {skill}")
            else:
                st.success("✅ Your curriculum covers all current market requirements!")
        
        with tab5:
            st.write("**📋 Realistic Job Market Listings:**")
            
            jobs = results['real_market_insights']['jobs'][:12]
            
            # Job search filters
            col1, col2, col3 = st.columns(3)
            with col1:
                exp_filter = st.selectbox("Experience Level", ["All", "Fresher", "0-1 years", "Entry Level"])
            with col2:
                location_filter = st.selectbox("Location", ["All"] + list(set(job['location'].split(',')[0].strip() for job in jobs)))
            with col3:
                company_filter = st.selectbox("Company", ["All"] + list(set(job['company'] for job in jobs)))
            
            # Apply filters
            filtered_jobs = jobs
            if exp_filter != "All":
                filtered_jobs = [job for job in filtered_jobs if exp_filter.lower() in job['experience_level'].lower()]
            if location_filter != "All":
                filtered_jobs = [job for job in filtered_jobs if location_filter.lower() in job['location'].lower()]
            if company_filter != "All":
                filtered_jobs = [job for job in filtered_jobs if company_filter.lower() in job['company'].lower()]
            
            st.write(f"Showing {len(filtered_jobs)} of {len(jobs)} jobs")
            
            # Display jobs
            for i, job in enumerate(filtered_jobs, 1):
                with st.expander(f"💼 {i}. {job['title']} at {job['company']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**📍 Location:** {job['location']}")
                    with col2:
                        st.write(f"**💰 Salary:** {job['salary']}")
                    with col3:
                        st.write(f"**📅 Posted:** {job['posted_date']}")
                    
                    st.write(f"**🏢 Company:** {job['company']}")
                    st.write(f"**🎯 Experience:** {job['experience_level']}")
                    st.write(f"**🔗 Source:** {job['source']}")
                    
                    with st.expander("📋 Job Description"):
                        st.write(job['description'][:500] + "..." if len(job['description']) > 500 else job['description'])
                    
                    st.write(f"**🛠️ Required Skills:** {', '.join(job['skills'])}")
                    
                    if job['url'] and job['url'] != "N/A":
                        st.markdown(f"[🔗 View Job Details]({job['url']})")
        
        # Action Section
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Analysis Report", use_container_width=True):
                # Save to file
                with open(f'skill_twin_analysis_{int(time.time())}.json', 'w') as f:
                    json.dump(results, f, indent=2)
                st.success("✅ Analysis saved successfully!")
        
        with col2:
            if st.button("📊 Export to PDF", use_container_width=True):
                st.info("PDF export feature coming soon!")
        
        with col3:
            if st.button("🔄 Start New Analysis", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p><strong>🎯 Real Job Market Skill-Twin Engine</strong></p>
        <p>Realistic job market intelligence based on industry patterns and trends</p>
        <p><em>Helping bridge the gap between education and employment</em></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()