import React, { useState } from 'react';
import { checkText } from '../api/writingService';
import ResultDisplay from '../components/ResultDisplay';
import InputBox from '../components/InputBox';

function HomePage() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  /**
   * Hàm này được truyền xuống InputBox và sẽ được gọi khi
   * người dùng nhấn nút "Submit".
   * @param {string} text - Văn bản nhận về từ InputBox.
   */
  const handleSubmit = async (text) => {
    setIsLoading(true);
    setApiError(null);
    setResult(null);
    
    try {
      const data = await checkText(text);
      setResult(data);
    } catch (err) {
      setApiError(err.detail || 'Đã xảy ra lỗi khi phân tích.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="homepage-container">
      <h1>AI English Writing Tutor</h1>
      <p>Nhập bài viết của bạn để nhận phản hồi chi tiết từ AI.</p>
      
      {/* Sử dụng component InputBox thay vì code trực tiếp */}
      <InputBox onSubmit={handleSubmit} isLoading={isLoading} />

      {/* Hiển thị lỗi API (nếu có) */}
      {apiError && <div className="error-message">{apiError}</div>}
      
      {/* Hiển thị kết quả */}
      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default HomePage;