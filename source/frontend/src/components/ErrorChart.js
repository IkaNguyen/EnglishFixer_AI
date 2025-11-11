import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const ErrorChart = ({ commonErrors }) => {
  if (!commonErrors || commonErrors.length === 0) {
    return <p>Bạn chưa có lỗi nào để thống kê. Làm tốt lắm!</p>;
  }

  const data = {
    labels: commonErrors.map(e => e.error_type),
    datasets: [
      {
        label: '# of Errors',
        data: commonErrors.map(e => e.count),
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto' }}>
      <Pie data={data} />
    </div>
  );
};

export default ErrorChart;