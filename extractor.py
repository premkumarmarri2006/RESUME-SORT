import re
from typing import List, Dict

COMMON_SKILLS = {
    "python", "java", "javascript", "react", "node.js", "c++", "c#", "ruby", "go",
    "rust", "sql", "nosql", "mongodb", "postgresql", "mysql", "docker", "kubernetes",
    "aws", "azure", "gcp", "machine learning", "deep learning", "ai", "nlp",
    "data science", "data engineering", "devops", "ci/cd", "git", "linux",
    "html", "css", "tailwind", "fastapi", "django", "flask", "spring boot", "agile",
    "scrum", "typescript", "vue", "angular", "redis", "kafka", "terraform",
    "spark", "hadoop", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "rest", "graphql", "microservices", "project management", "leadership", "communication"
}

def extract_email(text: str) -> str:
    m = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return m.group(0) if m else "Not Found"

def extract_name(text: str) -> str:
    for line in text.strip().split('\n')[:5]:
        line = line.strip()
        if (2 < len(line) <= 50 and len(line.split()) <= 5 and
                not re.search(r'[\d@|]', line) and
                not re.search(r'(resume|curriculum|vitae|address|phone|email)', line, re.I)):
            return line.title()
    return "Unknown Candidate"

def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    return sorted([s.title() for s in COMMON_SKILLS
                   if re.search(r'\b' + re.escape(s) + r'\b', text_lower)])

def extract_experience(text: str) -> str:
    t = text.lower()
    if re.search(r'\b(senior|lead|principal|director|manager|head of|vp|vice president)\b', t):
        return "Senior"
    if re.search(r'\b(mid|intermediate)\b', t):
        return "Mid-Level"
    if re.search(r'\b(junior|entry|intern|fresher|graduate|student)\b', t):
        return "Entry-Level"
    m = re.search(r'(\d+)\+?\s*(years?|yrs?)\s*(of\s+)?experience', t)
    if m:
        y = int(m.group(1))
        return f"Senior ({y}+ yrs)" if y >= 5 else f"Mid-Level ({y}+ yrs)" if y >= 2 else f"Entry-Level ({y}+ yrs)"
    return "Not Specified"

def extract_education(text: str) -> str:
    t = text.lower()
    if re.search(r'\b(phd|ph\.d|doctorate)\b', t): return "PhD"
    if re.search(r'\b(master|ms|m\.s|mba|m\.eng)\b', t): return "Master's Degree"
    if re.search(r'\b(bachelor|bs|b\.s|ba|btech|b\.tech|bsc|b\.eng)\b', t): return "Bachelor's Degree"
    if re.search(r'\b(associate|diploma|certificate)\b', t): return "Associate/Diploma"
    return "Not Specified"

def extract_structured_data(text: str) -> Dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
    }
