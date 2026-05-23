import re
from typing import List, Tuple

# Flat import
from extractor import COMMON_SKILLS

# Try to load ML model, fall back to keyword scoring if unavailable
try:
    from sentence_transformers import SentenceTransformer, util as st_util
    _model = SentenceTransformer('all-MiniLM-L6-v2')
    ML_AVAILABLE = True
    print("✅ SentenceTransformer loaded.")
except Exception as e:
    print(f"⚠️  ML model unavailable ({e}). Using keyword scorer.")
    ML_AVAILABLE = False


def get_skill_overlap(job_description: str, resume_skills: List[str]) -> Tuple[List[str], List[str]]:
    jd_lower = job_description.lower()
    jd_skills = [s for s in COMMON_SKILLS if re.search(r'\b' + re.escape(s) + r'\b', jd_lower)]
    resume_lower = [s.lower() for s in resume_skills]
    matched = [s.title() for s in jd_skills if s.lower() in resume_lower]
    missing = [s.title() for s in jd_skills if s.lower() not in resume_lower]
    return matched, missing


def compute_similarity(job_description: str, resume_text: str) -> float:
    if not job_description or not resume_text:
        return 0.0
    if ML_AVAILABLE:
        try:
            jd_emb = _model.encode(job_description[:2000], convert_to_tensor=True)
            res_emb = _model.encode(resume_text[:2000], convert_to_tensor=True)
            cos = st_util.cos_sim(jd_emb, res_emb)[0][0].item()
            return min(100.0, max(0.0, round((cos + 1) / 2 * 100, 1)))
        except Exception as e:
            print(f"ML scoring failed: {e}")
    # Keyword fallback
    jd_words = set(re.findall(r'\b\w{3,}\b', job_description.lower()))
    res_words = set(re.findall(r'\b\w{3,}\b', resume_text.lower()))
    if not jd_words:
        return 0.0
    return min(100.0, round(len(jd_words & res_words) / len(jd_words) * 100, 1))


def generate_explanation(score: float, matched: List[str], missing: List[str]) -> str:
    if score >= 75:
        base = "🟢 Strong match."
    elif score >= 50:
        base = "🟡 Good match."
    elif score >= 30:
        base = "🟠 Moderate match."
    else:
        base = "🔴 Weak match."
    if matched:
        base += f" Strengths: {', '.join(matched[:4])}."
    if missing:
        base += f" Gaps: {', '.join(missing[:4])}."
    return base


def calculate_confidence(text_length: int, score: float) -> float:
    confidence = 95.0
    if text_length < 200:
        confidence -= 50.0
    elif text_length < 500:
        confidence -= 25.0
    elif text_length < 800:
        confidence -= 10.0
    if score == 0.0:
        confidence -= 20.0
    return max(0.0, min(100.0, round(confidence, 1)))
