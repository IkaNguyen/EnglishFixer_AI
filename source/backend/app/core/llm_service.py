import google.generativeai as genai
import json
from .config import settings
from .prompts import get_feedback_prompt
from ..schemas.submission import TextSubmissionResponse, FeedbackDetail

# Cấu hình Gemini API
try:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("Gemini API configured.")
except Exception as e:
    print(f"Lỗi cấu hình Gemini: {e}")
    model = None

def clean_json_response(raw_response: str) -> dict:
    """Làm sạch text trả về từ LLM để đảm bảo nó là JSON hợp lệ."""
    cleaned_text = raw_response.strip().replace('```json', '').replace('```', '').strip()
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"Lỗi phân tích JSON: {e}")
        raise ValueError(f"Không thể phân tích JSON từ LLM: {cleaned_text}")

async def get_llm_feedback(text: str) -> TextSubmissionResponse:
    if not model:
        raise Exception("Mô hình LLM chưa được khởi tạo.")

    prompt = get_feedback_prompt(text)
    
    try:
        response = model.generate_content(prompt)
        json_data = clean_json_response(response.text)
        
        # Validate dữ liệu bằng Pydantic
        return TextSubmissionResponse(**json_data)
        
    except Exception as e:
        print(f"Lỗi khi gọi LLM: {e}")
        # Trả về lỗi theo cấu trúc để frontend có thể xử lý
        raise ValueError(f"Có lỗi xảy ra khi phân tích bài viết: {e}")