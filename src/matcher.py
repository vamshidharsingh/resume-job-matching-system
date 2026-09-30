import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, Any, List

# Load model globally to avoid reloading on every request
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    """Get sentence embedding for text."""
    embedding = model.encode([text])[0]
    return embedding

def compute_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Compute semantic similarity between resume and JD using FAISS."""
    if not resume_text or not jd_text:
        return 0.0
        
    resume_emb = get_embedding(resume_text).astype('float32')
    jd_emb = get_embedding(jd_text).astype('float32')
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(np.array([resume_emb]))
    faiss.normalize_L2(np.array([jd_emb]))
    
    # Create FAISS index
    d = resume_emb.shape[0]
    index = faiss.IndexFlatIP(d) # Inner product with normalized vectors = cosine similarity
    index.add(np.array([jd_emb]))
    
    # Search
    D, I = index.search(np.array([resume_emb]), 1)
    
    similarity = float(D[0][0])
    # Ensure it's between 0 and 1
    return max(0.0, min(1.0, similarity))

def calculate_match_score(resume_skills: set, jd_skills: set, semantic_sim: float) -> Dict[str, Any]:
    """
    Calculate an overall match score and provide transparent insights.
    Combines direct skill overlap with semantic similarity.
    """
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)
    
    # Skill score: percentage of JD skills found in resume
    if jd_skills:
        skill_score = len(matched_skills) / len(jd_skills)
    else:
        skill_score = 1.0 if not missing_skills else 0.0
        
    # Weighted combination: 60% skills, 40% semantic context
    overall_score = (skill_score * 0.6) + (semantic_sim * 0.4)
    
    return {
        "overall_score_percentage": round(overall_score * 100, 2),
        "skill_match_percentage": round(skill_score * 100, 2),
        "semantic_similarity_percentage": round(semantic_sim * 100, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills)
    }
