import React, { useState, useEffect } from 'react';
import { getDashboardStats } from '../api/userService';
import ErrorChart from '../components/ErrorChart';

function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getDashboardStats();
        setStats(data);
      } catch (err) {
        setError('Không thể tải dữ liệu thống kê.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []); // Chạy 1 lần khi component được mount

  if (loading) {
    return <div>Đang tải dữ liệu...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="dashboard-container">
      <h2>Bảng điều khiển của bạn</h2>
      
      <h3>Tổng số bài đã nộp: {stats?.total_submissions || 0}</h3>

      <h3>Các lỗi sai phổ biến nhất</h3>
      <ErrorChart commonErrors={stats?.common_errors} />
    </div>
  );
}

export default DashboardPage;