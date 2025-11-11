import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './views/HomePage';
import LoginPage from './views/LoginPage'; 
import DashboardPage from './views/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';
import './assets/styles/main.css';

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Tuyến đường công khai (Public) */}
        <Route path="/login" element={<LoginPage />} />

        {/* Tuyến đường được bảo vệ (Protected)
          - Mọi route con bên trong <ProtectedRoute />
          - sẽ yêu cầu đăng nhập.
        */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          {/* có thể thêm các trang cần bảo vệ khác ở đây */}
          {/* <Route path="/history" element={<HistoryPage />} /> */}
        </Route>
        
        {/* (có thể thêm trang 404 Not Found ở đây) */}
      </Routes>
    </div>
  );
}

export default App;