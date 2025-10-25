import React from 'react';

function ResultDisplay({ result }) {
  if (!result) return null;

  return (
    <div className="result-container">
      
      {/* 1. Bài viết đã sửa */}
      <h2>Bài viết đã sửa (Corrected)</h2>
      <div className="corrected-text">
        <p>{result.corrected_text}</p>
      </div>
      
      {/* 2. Các góp ý chi tiết */}
      <h2>Góp ý chi tiết (Feedback Details)</h2>
      <div className="feedback-list">
        {result.feedback_details.map((item, index) => (
          <div className="feedback-card" key={index}>
            <span className="error-type">{item.error_type}</span>
            <p><strong>Lỗi:</strong> <del>{item.original_phrase}</del></p>
            <p><strong>Gợi ý:</strong> <ins>{item.suggestion}</ins></p>
            <p><strong>Giải thích:</strong> {item.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResultDisplay;