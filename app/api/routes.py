from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import AnalysisResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import calculate_similarity_score
from app.services.llm_service import generate_cv_feedback

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_cv(
    cv_file: UploadFile = File(...), 
    job_description: str = Form(...)
):
    if not cv_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        file_bytes = await cv_file.read()
        
        # Phase 2 Engine: Extract Text
        cv_text = extract_text_from_pdf(file_bytes)
        
        # Phase 3a Engine: Calculate Semantic Baseline
        nlp_score = calculate_similarity_score(cv_text, job_description)
        
        # Phase 3b Engine: LLM Calibration and Synthesis
        final_json = generate_cv_feedback(cv_text, job_description, nlp_score)
        
        return final_json
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")