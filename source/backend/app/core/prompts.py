def get_feedback_prompt(user_text: str) -> str:
    """
    Tạo prompt chi tiết để LLM phân tích và trả về JSON.
    """
    return f"""
    You are an expert English teacher specializing in helping Vietnamese learners.
    Analyze the student's text below.

    **Student's Text:**
    "{user_text}"

    **Your Task:**
    Provide the response in a clean JSON format with three keys: "corrected_text", "original_text", and "feedback_details".
    - "corrected_text": The corrected, natural-sounding version of the text.
    - "original_text": The student's original text.
    - "feedback_details": A list of JSON objects. Each object must have "error_type", "original_phrase", "suggestion", and "explanation" (in simple Vietnamese).

    Please begin your JSON response now.
    """