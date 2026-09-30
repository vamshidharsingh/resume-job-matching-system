import pytest
from src.nlp import extract_skills
from src.matcher import calculate_match_score, compute_semantic_similarity

def test_extract_skills():
    text = "I have 5 years of experience in Python and machine learning. I also know SQL."
    skills = extract_skills(text)
    assert "python" in skills
    assert "machine learning" in skills
    assert "sql" in skills
    assert "java" not in skills

def test_calculate_match_score():
    resume_skills = {"python", "machine learning", "sql"}
    jd_skills = {"python", "machine learning", "docker"}
    
    result = calculate_match_score(resume_skills, jd_skills, 0.8)
    
    # matched = python, machine learning (2)
    # missing = docker (1)
    # skill score = 2/3 = 0.666...
    # overall = (0.666 * 0.6) + (0.8 * 0.4) = 0.4 + 0.32 = 0.72
    
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]
    assert result["skill_match_percentage"] == round((2/3) * 100, 2)
    assert result["semantic_similarity_percentage"] == 80.0
    assert result["overall_score_percentage"] == round(0.72 * 100, 2)

def test_compute_semantic_similarity():
    text1 = "Software engineer building web applications"
    text2 = "Web developer creating scalable software"
    sim = compute_semantic_similarity(text1, text2)
    
    assert 0.0 <= sim <= 1.0
    assert type(sim) == float
