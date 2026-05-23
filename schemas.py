from pydantic import BaseModel
from typing import List

class ExtractedData(BaseModel):
    name: str = "Unknown Candidate"
    email: str = "Not Found"
    skills: List[str] = []
    experience: str = "Not Specified"
    education: str = "Not Specified"

class ResumeResult(BaseModel):
    filename: str
    size: str
    score: float
    rank: int = 0
    snippet: str
    full_text: str
    extracted_data: ExtractedData
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    explanation: str = ""
    confidence_score: float = 0.0

class AnalysisResponse(BaseModel):
    job_description: str
    ranked_resumes: List[ResumeResult]
