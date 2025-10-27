import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * Component này kiểm tra xem người dùng đã đăng nhập chưa.
 * - Nếu ĐÃ đăng nhập: Hiển thị nội dung (thông qua <Outlet />).
 * - Nếu CHƯA đăng nhập: Điều hướng về trang /login.
 */
function ProtectedRoute() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    // Người dùng chưa đăng nhập, chuyển hướng về trang Login
    // `replace` để người dùng không thể nhấn "Back" quay lại trang trước
    return <Navigate to="/login" replace />;
  }

  // Người dùng đã đăng nhập, cho phép truy cập
  // <Outlet /> sẽ render bất kỳ route con nào được định nghĩa trong App.js
  return <Outlet />;
}

export default ProtectedRoute;