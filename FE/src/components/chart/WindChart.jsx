import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "chartjs-adapter-luxon";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const WindChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index + 1), // 인덱스를 라벨로 사용
    datasets: [
      {
        label: "Wind Speed",
        data: data,
        borderColor: "rgba(255, 99, 132, 1)", // 빨간색
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        pointRadius: 1,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        title: {
          display: true,
          text: "Wind Speed",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default WindChart;
