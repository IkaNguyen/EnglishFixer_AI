from pydantic import BaseModel
from typing import List, Optional

class TextSubmissionRequest(BaseModel):
    text: str

class FeedbackDetail(BaseModel):
    error_type: str
    original_phrase: str
    suggestion: str
    explanation: str

class TextSubmissionResponse(BaseModel):
    original_text: str
    corrected_text: str
    feedback_details: List[FeedbackDetail]