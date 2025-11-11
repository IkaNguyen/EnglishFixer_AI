import axios from 'axios';

// (Giả sử bạn có một interceptor của axios để tự động
// đính kèm token vào header 'Authorization')

const API_URL = process.env.REACT_APP_BACKEND_API_URL;

/**
 * Lấy dữ liệu thống kê cho trang Dashboard.
 */
export const getDashboardStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/me/dashboard-stats`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
    throw error;
  }
};