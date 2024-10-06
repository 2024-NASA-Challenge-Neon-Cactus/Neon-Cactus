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

const NoiseChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index + 1), // 인덱스를 라벨로 사용
    datasets: [
      {
        label: "Noise Level",
        data: data,
        borderColor: "rgba(153, 102, 255, 1)", // 보라색
        backgroundColor: "rgba(153, 102, 255, 0.2)",
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
          text: "Noise Level",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default NoiseChart;
