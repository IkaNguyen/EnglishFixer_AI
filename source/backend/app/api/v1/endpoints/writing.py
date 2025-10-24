from fastapi import APIRouter, HTTPException
from ....schemas.submission import TextSubmissionRequest, TextSubmissionResponse
from ....core import llm_service

router = APIRouter()

@router.post("/check-text", response_model=TextSubmissionResponse)
async def check_writing(request: TextSubmissionRequest):
    """
    Nhận văn bản từ người dùng và trả về phân tích từ LLM.
    """
    try:
        feedback = await llm_service.get_llm_feedback(request.text)
        return feedback
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {e}")