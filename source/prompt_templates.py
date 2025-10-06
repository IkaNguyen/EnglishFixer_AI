def create_feedback_prompt(user_text):
    """
    Tạo prompt chi tiết để LLM phân tích và đưa ra phản hồi.
    """
    prompt = f"""
    You are an expert English teacher specializing in helping Vietnamese learners. 
    Your student has written the following text. Please analyze it carefully.

    **Student's Text:**
    "{user_text}"

    **Your Task (provide the response in JSON format with the following keys: "original_text", "corrected_text", "feedback_details"):**

    1.  **"original_text"**: The original text written by the student.
    2.  **"corrected_text"**: Provide a corrected version of the text that sounds natural and fluent.
    3.  **"feedback_details"**: Provide a list of specific feedback points. Each point in the list should be a JSON object with these keys: "error_type", "original_phrase", "suggestion", and "explanation".
        * "error_type": Classify the error (e.g., "Grammar", "Vocabulary Choice", "Punctuation", "Awkward Phrasing").
        * "original_phrase": The exact phrase from the student's text that contains the error.
        * "suggestion": The corrected phrase.
        * "explanation": A simple, clear explanation in VIETNAMESE about why it was wrong and how the suggestion improves it. This explanation should be tailored for a Vietnamese learner, possibly referencing common L1 interference issues.

    **Example of a feedback_details object:**
    {{
      "error_type": "Grammar",
      "original_phrase": "I am interesting in this movie.",
      "suggestion": "I am interested in this movie.",
      "explanation": "Trong tiếng Anh, khi muốn diễn tả cảm xúc hoặc sự quan tâm của bản thân, chúng ta dùng tính từ đuôi '-ed' (interested). Tính từ đuôi '-ing' (interesting) dùng để mô tả bản chất của sự vật, sự việc (bộ phim này thú vị)."
    }}

    Please begin your analysis now.
    """
    return prompt