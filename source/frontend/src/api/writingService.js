import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_API_URL;

export const checkText = async (text) => {
  try {
    // Gọi đến endpoint /check-text đã tạo ở phần backend
    const response = await axios.post(`${API_URL}/check-text`, {
      text: text,
    });
    return response.data; // Trả về đối tượng JSON
  } catch (error) {
    // Ném lỗi ra để component có thể bắt
    throw error.response?.data || new Error('Không thể kết nối đến máy chủ API');
  }
};