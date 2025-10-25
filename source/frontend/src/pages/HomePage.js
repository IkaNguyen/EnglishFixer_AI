import React, { useState } from 'react';
import { checkText } from '../api/writingService';
import ResultDisplay from '../components/ResultDisplay';

function HomePage() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Vui lòng nhập văn bản.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const data = await checkText(text);
      setResult(data);
    } catch (err) {
      setError(err.detail || 'Đã xảy ra lỗi khi phân tích.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="homepage-container">
      <h1>AI English Writing Tutor</h1>
      <p>Nhập bài viết của bạn để nhận phản hồi chi tiết từ AI.</p>
      
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Start writing here..."
        disabled={isLoading}
      />
      
      <button onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Đang phân tích...' : 'Kiểm tra bài viết'}
      </button>

      {/* Hiển thị lỗi nếu có */}
      {error && <div className="error-message">{error}</div>}
      
      {/* Hiển thị kết quả */}
      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default HomePage;