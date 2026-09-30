import fitz  # PyMuPDF
import spacy
import re

# Load spacy model, fallback to downloading if not present
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

def extract_skills(text: str, predefined_skills: set = None) -> set:
    """
    Extract skills from text using NLP and regex.
    """
    if predefined_skills is None:
        predefined_skills = {
            "python", "java", "c++", "machine learning", "nlp", "spacy", 
            "fastapi", "streamlit", "aws", "docker", "kubernetes", 
            "sql", "nosql", "pytorch", "tensorflow", "scikit-learn", 
            "data analysis", "react", "javascript", "typescript", "html", "css",
            "git", "ci/cd", "agile", "pandas", "numpy", "faiss"
        }
    
    text_lower = text.lower()
    found_skills = set()
    
    # Simple keyword matching
    for skill in predefined_skills:
        # Use word boundaries for exact matching, escape special characters
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    # Using spaCy to extract entities that might be skills/technologies
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            candidate = ent.text.lower()
            if len(candidate) > 2 and len(candidate.split()) <= 2:
                # In a full system, you might validate against a larger database here
                pass
                
    return found_skills
