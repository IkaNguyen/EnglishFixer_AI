import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from prompt_templates import create_feedback_prompt

# Tải các biến môi trường từ file .env
load_dotenv()

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình Google Gemini API
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

# Định nghĩa API endpoint
@app.route('/analyze', methods=['POST'])
def analyze_text():
    if not model:
        return jsonify({"error": "Gemini API is not configured."}), 500

    # Lấy dữ liệu JSON từ request
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body."}), 400

    user_text = data['text']

    # Tạo prompt
    prompt = create_feedback_prompt(user_text)

    try:
        # Gửi prompt đến Gemini và nhận phản hồi
        response = model.generate_content(prompt)
        
        # LLM có thể trả về văn bản có chứa markdown, cần làm sạch
        cleaned_response_text = response.text.replace('```json', '').replace('```', '').strip()
        
        # Chuyển đổi chuỗi JSON thành đối tượng Python
        feedback_data = json.loads(cleaned_response_text)
        
        return jsonify(feedback_data)

    except json.JSONDecodeError:
        # Xử lý lỗi nếu LLM không trả về JSON hợp lệ
        return jsonify({"error": "Failed to parse LLM response.", "raw_response": response.text}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Chạy ứng dụng
if __name__ == '__main__':
    # Chạy ở chế độ debug để dễ dàng phát triển
    app.run(debug=True, port=5001)