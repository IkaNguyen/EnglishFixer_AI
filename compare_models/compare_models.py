import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

# Tải các biến môi trường từ file .env
load_dotenv()

# --- CẤU HÌNH CÁC CLIENT ---
try:
    # Cấu hình Gemini
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    gemini_model = genai.GenerativeModel('gemini-2.5-pro')

    # Cấu hình Groq (cho Llama 3)
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    llama_model_name = "llama-3.3-70b-versatile"
    
    print("API clients configured successfully.")
except Exception as e:
    print(f"Error configuring API clients: {e}")
    exit()

# --- DỮ LIỆU ĐẦU VÀO VÀ PROMPT ---

# Đoạn văn bản tiếng Anh có lỗi sai để kiểm thử
USER_TEXT = "I am very interesting in this lesson, but it make me feel confuse. I hope learn more."

# Prompt chung cho cả hai mô hình, yêu cầu trả về định dạng JSON
PROMPT_TEMPLATE = """
You are an expert English teacher specializing in helping Vietnamese learners.
Analyze the student's text below.

**Student's Text:**
"{user_text}"

**Your Task:**
Provide the response in a clean JSON format with three keys: "corrected_text", "original_text", and "feedback_details".
- "corrected_text": The corrected, natural-sounding version of the text.
- "original_text": The student's original text.
- "feedback_details": A list of JSON objects. Each object must have "error_type", "original_phrase", "suggestion", and "explanation" (in simple Vietnamese).

Please start your JSON response now.
"""

# --- CÁC HÀM GỌI API ĐÃ NÂNG CẤP ---

def get_feedback_from_gemini(text, prompt_template):
    """
    Gửi yêu cầu đến Gemini và trả về một dictionary chứa các chỉ số.
    """
    print("Requesting from Gemini...")
    start_time = time.time()
    try:
        prompt = prompt_template.format(user_text=text)
        response = gemini_model.generate_content(prompt)
        latency = time.time() - start_time
        
        # Trích xuất thông tin sử dụng token
        usage = response.usage_metadata
        token_usage = {
            "prompt_tokens": usage.prompt_token_count,
            "completion_tokens": usage.candidates_token_count
        }
        
        return {
            "status": "success",
            "latency": latency,
            "raw_response": response.text,
            "usage": token_usage
        }
    except Exception as e:
        latency = time.time() - start_time
        return {
            "status": "error",
            "latency": latency,
            "error_message": str(e),
            "usage": {"prompt_tokens": 0, "completion_tokens": 0}
        }

def get_feedback_from_llama(text, prompt_template):
    """
    Gửi yêu cầu đến Llama 3 (qua Groq) và trả về một dictionary chứa các chỉ số.
    """
    print("Requesting from Llama 3 (via Groq)...")
    start_time = time.time()
    try:
        prompt = prompt_template.format(user_text=text)
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=llama_model_name,
            temperature=0.1, # Đặt temp thấp để tăng tính nhất quán
        )
        latency = time.time() - start_time
        
        # Trích xuất thông tin sử dụng token
        usage = chat_completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens
        }

        return {
            "status": "success",
            "latency": latency,
            "raw_response": chat_completion.choices[0].message.content,
            "usage": token_usage
        }
    except Exception as e:
        latency = time.time() - start_time
        return {
            "status": "error",
            "latency": latency,
            "error_message": str(e),
            "usage": {"prompt_tokens": 0, "completion_tokens": 0}
        }

def parse_json_response(raw_response):
    """
    Thử phân tích cú pháp JSON và trả về trạng thái.
    """
    try:
        # LLM có thể trả về văn bản có chứa markdown, cần làm sạch
        cleaned_text = raw_response.strip().replace('```json', '').replace('```', '').strip()
        parsed_data = json.loads(cleaned_text)
        return {"is_valid_json": True, "parsed_data": parsed_data}
    except json.JSONDecodeError:
        return {"is_valid_json": False, "parsed_data": None}

# --- CHẠY ĐÁNH GIÁ ---
if __name__ == "__main__":
    print("--- Bắt đầu chạy Đánh giá So sánh Mô hình ---")
    
    # --- Chạy Lần 1 (Để lấy kết quả và đo lường) ---
    print("\n--- Lần chạy 1 (Đo lường chính) ---")
    gemini_run1 = get_feedback_from_gemini(USER_TEXT, PROMPT_TEMPLATE)
    llama_run1 = get_feedback_from_llama(USER_TEXT, PROMPT_TEMPLATE)

    # --- Chạy Lần 2 (Để kiểm tra tính nhất quán) ---
    print("\n--- Lần chạy 2 (Kiểm tra Tính nhất quán) ---")
    gemini_run2 = get_feedback_from_gemini(USER_TEXT, PROMPT_TEMPLATE)
    llama_run2 = get_feedback_from_llama(USER_TEXT, PROMPT_TEMPLATE)
    
    # --- Tổng hợp Chỉ số Kỹ thuật ---
    summary = {
        "gemini": {
            "latency_run1_s": gemini_run1.get('latency', 0),
            "is_valid_json": False,
            "is_consistent": False,
            "token_usage": gemini_run1.get('usage', {})
        },
        "llama": {
            "latency_run1_s": llama_run1.get('latency', 0),
            "is_valid_json": False,
            "is_consistent": False,
            "token_usage": llama_run1.get('usage', {})
        }
    }
    
    # Kiểm tra tính hợp lệ của JSON (Lần chạy 1)
    if gemini_run1['status'] == 'success':
        summary['gemini']['is_valid_json'] = parse_json_response(gemini_run1['raw_response'])['is_valid_json']
    if llama_run1['status'] == 'success':
        summary['llama']['is_valid_json'] = parse_json_response(llama_run1['raw_response'])['is_valid_json']
        
    # Kiểm tra tính nhất quán (So sánh Lần 1 và Lần 2)
    if gemini_run1['status'] == 'success' and gemini_run2['status'] == 'success':
        summary['gemini']['is_consistent'] = (gemini_run1['raw_response'] == gemini_run2['raw_response'])
    if llama_run1['status'] == 'success' and llama_run2['status'] == 'success':
        summary['llama']['is_consistent'] = (llama_run1['raw_response'] == llama_run2['raw_response'])

    # --- In Bảng tổng kết Chỉ số Kỹ thuật & Chi phí ---
    print("\n\n" + "="*50)
    print(" BẢNG TỔNG KẾT CHỈ SỐ (KỸ THUẬT & CHI PHÍ)")
    print("="*50)
    
    print("\n--- Google Gemini ---")
    print(f"  Tốc độ phản hồi (Latency):  {summary['gemini']['latency_run1_s']:.2f} giây")
    print(f"  Tuân thủ JSON (Valid JSON): {summary['gemini']['is_valid_json']}")
    print(f"  Tính nhất quán (Consistent): {summary['gemini']['is_consistent']}")
    print(f"  Sử dụng Token (Input):      {summary['gemini']['token_usage'].get('prompt_tokens', 0)} tokens")
    print(f"  Sử dụng Token (Output):     {summary['gemini']['token_usage'].get('completion_tokens', 0)} tokens")

    print("\n--- Meta Llama 3 (via Groq) ---")
    print(f"  Tốc độ phản hồi (Latency):  {summary['llama']['latency_run1_s']:.2f} giây")
    print(f"  Tuân thủ JSON (Valid JSON): {summary['llama']['is_valid_json']}")
    print(f"  Tính nhất quán (Consistent): {summary['llama']['is_consistent']}")
    print(f"  Sử dụng Token (Input):      {summary['llama']['token_usage'].get('prompt_tokens', 0)} tokens")
    print(f"  Sử dụng Token (Output):     {summary['llama']['token_usage'].get('completion_tokens', 0)} tokens")
    
    print("\n\n" + "="*50)
    print(" PHẢN HỒI CHI TIẾT (ĐỂ ĐÁNH GIÁ CHẤT LƯỢNG)")
    print("="*50)

    # --- In Kết quả JSON (Lần chạy 1) để Đánh giá Thủ công ---
    
    print("\n--- ✅ KẾT QUẢ TỪ Google Gemini ---")
    if gemini_run1['status'] == 'success':
        json_check = parse_json_response(gemini_run1['raw_response'])
        if json_check['is_valid_json']:
            print(json.dumps(json_check['parsed_data'], indent=2, ensure_ascii=False))
        else:
            print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
            print(gemini_run1['raw_response'])
    else:
        print(f"Lỗi API: {gemini_run1['error_message']}")

    print("\n--- ✅ KẾT QUẢ TỪ Meta Llama 3 ---")
    if llama_run1['status'] == 'success':
        json_check = parse_json_response(llama_run1['raw_response'])
        if json_check['is_valid_json']:
            print(json.dumps(json_check['parsed_data'], indent=2, ensure_ascii=False))
        else:
            print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
            print(llama_run1['raw_response'])
    else:
        print(f"Lỗi API: {llama_run1['error_message']}")