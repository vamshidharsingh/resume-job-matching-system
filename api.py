from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from typing import List

from src.nlp import extract_text_from_pdf, extract_skills
from src.matcher import compute_semantic_similarity, calculate_match_score

app = FastAPI(title="AI Resume Matching API")

class MatchResponse(BaseModel):
    overall_score_percentage: float
    skill_match_percentage: float
    semantic_similarity_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/match", response_model=MatchResponse)
async def match_resume_to_jd(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    try:
        # Read PDF
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        
        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_description)
        
        # Compute Semantic Similarity
        semantic_sim = compute_semantic_similarity(resume_text, job_description)
        
        # Calculate Final Score
        result = calculate_match_score(resume_skills, jd_skills, semantic_sim)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8004, reload=True)
