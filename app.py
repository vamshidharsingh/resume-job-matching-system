import streamlit as st
import requests

API_URL = "http://localhost:8004/match"

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume & Job Matching System")
st.markdown("Upload a candidate's resume and provide a job description to see how well they match.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    job_description = st.text_area("Paste the job description here", height=300)

with col2:
    st.subheader("2. Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF format only)", type="pdf")

if st.button("Analyze Match", type="primary"):
    if not job_description:
        st.warning("Please provide a job description.")
    elif not uploaded_file:
        st.warning("Please upload a resume.")
    else:
        with st.spinner("Analyzing resume and computing match scores..."):
            try:
                # Prepare payload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"job_description": job_description}
                
                # Make request to API
                response = requests.post(API_URL, files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    # Display results
                    st.header("Match Insights")
                    
                    # Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Overall Match Score", f"{result['overall_score_percentage']}%")
                    m2.metric("Skill Overlap", f"{result['skill_match_percentage']}%")
                    m3.metric("Semantic Relevance", f"{result['semantic_similarity_percentage']}%")
                    
                    # Progress bar for overall score
                    st.progress(result['overall_score_percentage'] / 100)
                    
                    # Skills
                    st.subheader("Skill Analysis")
                    s1, s2 = st.columns(2)
                    
                    with s1:
                        st.markdown("### ✅ Matched Skills")
                        if result['matched_skills']:
                            for skill in result['matched_skills']:
                                st.markdown(f"- {skill.title()}")
                        else:
                            st.info("No common skills found.")
                            
                    with s2:
                        st.markdown("### ❌ Missing Skills")
                        if result['missing_skills']:
                            for skill in result['missing_skills']:
                                st.markdown(f"- {skill.title()}")
                        else:
                            st.info("No missing skills!")
                            
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend API. Make sure it's running on port 8004. Error: {str(e)}")
