# SKILL-TWIN: Learning Path Recommemnder

## 1. Introduction

SKILL-TWIN is an intelligent academic–industry alignment system designed to identify skill gaps between a student’s current capabilities and real-world job market requirements. It analyzes live job descriptions, university syllabus content, and the student’s academic and project portfolio to generate a personalized upskilling roadmap ("Bridge Course").

The core idea is to create a **digital twin of a student’s skill profile** and continuously compare it with evolving industry expectations.

---

## 2. Problem Statement

Universities often follow static syllabi, while the job market evolves rapidly. Students graduate with theoretical knowledge but lack role-specific, industry-relevant micro-skills. This leads to:

* Poor placement outcomes
* Skill mismatch with job roles
* Wasted time learning irrelevant content

There is no automated system that dynamically maps:

* Job market skill demand
* University syllabus coverage
* Individual student readiness

---

## 3. Proposed Solution

SKILL-TWIN bridges this gap by:

1. Scraping real job descriptions for a target role (e.g., Full Stack Developer, ML Engineer)
2. Extracting required skills using NLP
3. Comparing them with:

   * University syllabus
   * Student CGPA
   * GitHub repositories and projects
4. Generating a **personalized, prioritized learning roadmap**

---

## 4. System Objectives

* Align academic learning with industry needs
* Provide role-based skill gap analysis
* Offer personalized learning recommendations
* Improve employability and placement readiness

---

## 5. SDG Alignment

**UN SDG 4 – Quality Education**

* Ensures inclusive and equitable quality education
* Promotes lifelong learning opportunities
* Modernizes curriculum relevance using real-world data

---

## 6. System Architecture (High-Level)

1. Data Collection Layer

   * Job descriptions (LinkedIn/Naukri – scraped or mocked)
   * University syllabus (PDF/Text)
   * Student data (CGPA, GitHub, projects)

2. Processing Layer

   * Skill extraction using NLP
   * Skill normalization and categorization
   * Gap analysis engine

3. Recommendation Engine

   * Missing micro-skills detection
   * Priority scoring
   * Bridge course generation

4. Frontend Interface

   * Dashboard view
   * Skill gap visualization
   * Personalized roadmap

---

## 7. Key Features

* Role-specific analysis
* Live industry skill mapping
* CGPA-aware recommendations
* GitHub/project-based skill validation
* Actionable learning roadmap

---

## 8. Technology Stack

**Frontend:** React, HTML, CSS, JavaScript
**Backend:** Python (Flask/FastAPI) or Node.js
**NLP:** spaCy / NLTK / Transformers (basic level)
**Database:** SQLite / MongoDB
**Scraping:** BeautifulSoup / Selenium (or static dataset for demo)

---

## 9. Use Case Scenario

1. Student selects target role (e.g., Data Analyst)
2. System fetches relevant job descriptions
3. Skills are extracted and ranked
4. Student’s syllabus and projects are analyzed
5. Skill gaps are identified
6. A personalized bridge course is generated

---

## 10. Advantages

* Data-driven skill planning
* Reduces random course selection
* Improves placement readiness
* Scalable across roles and universities

---

## 11. Limitations

* Live scraping restrictions on some platforms
* Skill extraction accuracy depends on data quality
* Requires periodic updates for relevance

---

## 12. Future Enhancements

* AI-based skill proficiency scoring
* Resume optimization module
* Internship and course recommendations
* Integration with LinkedIn/GitHub APIs
* Real-time progress tracking dashboard

---

## 13. Conclusion

SKILL-TWIN acts as a smart academic companion that continuously aligns a student’s learning journey with industry demand. By transforming static education into a dynamic, personalized system, it enhances employability and supports sustainable, quality education.
