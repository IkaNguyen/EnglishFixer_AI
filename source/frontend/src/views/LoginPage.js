import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = () => {
    // (Đây là phần giả lập. Thực tế bạn sẽ gọi API /login)
    const fakeToken = 'day-la-mot-token-gia-lap-12345';
    login(fakeToken);
    
    // Đăng nhập thành công, điều hướng về trang chủ
    navigate('/');
  };

  return (
    <div>
      <h2>Login Page</h2>
      <p>This is a protected area. Please log in.</p>
      {/* (Bạn sẽ thay thế bằng form username/password thật)
      */}
      <button onClick={handleLogin}>Simulate Login</button>
    </div>
  );
}

export default LoginPage;