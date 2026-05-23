from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

# Flat imports — all files in same folder
from pdf_parser import extract_text_from_pdf
from docx_parser import extract_text_from_docx
from scorer import compute_similarity, get_skill_overlap, generate_explanation, calculate_confidence
from extractor import extract_structured_data
from db import db_client
from schemas import AnalysisResponse, ResumeResult, ExtractedData

router = APIRouter()


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


@router.post("/upload", response_model=AnalysisResponse)
async def upload_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    results = []

    for file in files:
        filename_lower = file.filename.lower()
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
            raise HTTPException(status_code=400, detail=f"'{file.filename}' must be PDF or DOCX.")

        content = await file.read()
        size_str = format_size(len(content))

        if filename_lower.endswith(".pdf"):
            text = extract_text_from_pdf(content)
        else:
            text = extract_text_from_docx(content)

        if not text or text.startswith("Error"):
            text = ""

        extracted = extract_structured_data(text)
        score = compute_similarity(job_description, text)
        matched_skills, missing_skills = get_skill_overlap(job_description, extracted["skills"])
        explanation = generate_explanation(score, matched_skills, missing_skills)
        confidence = calculate_confidence(len(text), score)
        snippet = (text[:400] + "...") if len(text) > 400 else text

        results.append(ResumeResult(
            filename=file.filename,
            size=size_str,
            score=round(score, 1),
            rank=0,
            snippet=snippet.strip(),
            full_text=text.strip(),
            extracted_data=ExtractedData(**extracted),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            explanation=explanation,
            confidence_score=confidence
        ))

    results.sort(key=lambda x: x.score, reverse=True)
    for i, res in enumerate(results):
        res.rank = i + 1

    top = results[0].extracted_data.name if results else "No candidate"
    db_client.save_search(job_description, len(files), top)

    return AnalysisResponse(job_description=job_description, ranked_resumes=results)


@router.get("/history")
async def get_history():
    return db_client.get_recent_searches()
