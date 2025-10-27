import React, { useState } from 'react';

/**
 * Component này quản lý ô nhập liệu và nút bấm.
 * @param {function} onSubmit - Hàm callback được gọi khi submit, trả về nội dung text.
 * @param {boolean} isLoading - Trạng thái loading để vô hiệu hóa form.
 */
function InputBox({ onSubmit, isLoading }) {
  const [text, setText] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = () => {
    if (!text.trim()) {
      setLocalError('Vui lòng nhập văn bản trước khi kiểm tra.');
      return;
    }
    setLocalError('');
    onSubmit(text); // Gửi text lên cho component cha (HomePage)
  };

  return (
    <div className="input-box-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Start writing here..."
        disabled={isLoading}
      />
      
      <button onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Đang phân tích...' : 'Kiểm tra bài viết'}
      </button>

      {localError && <div className="error-message-local">{localError}</div>}
    </div>
  );
}

export default InputBox;