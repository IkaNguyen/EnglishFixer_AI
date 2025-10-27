import React, { createContext, useState, useContext, useEffect } from 'react';

// Tạo Context
const AuthContext = createContext(null);

/**
 * Provider này sẽ "bọc" toàn bộ ứng dụng,
 * cung cấp thông tin đăng nhập cho mọi component con.
 */
export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);

  // Khi app mới tải, kiểm tra xem có token trong localStorage không
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
      // Bạn cũng nên cài đặt token này vào header của axios
      // axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  }, []);

  // Hàm đăng nhập
  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem('authToken', newToken);
    // axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  };

  // Hàm đăng xuất
  const logout = () => {
    setToken(null);
    localStorage.removeItem('authToken');
    // delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    token,
    login,
    logout,
    isAuthenticated: !!token, // Biến boolean tiện lợi
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Custom hook để component con dễ dàng lấy thông tin auth.
 * Thay vì phải import useContext và AuthContext mỗi lần.
 */
export const useAuth = () => {
  return useContext(AuthContext);
};