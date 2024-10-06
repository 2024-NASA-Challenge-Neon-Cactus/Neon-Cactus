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

const PressureChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index + 1), // 인덱스를 라벨로 사용
    datasets: [
      {
        label: "Pressure (hPa)",
        data: data,
        borderColor: "rgba(54, 162, 235, 1)", // 파란색
        backgroundColor: "rgba(54, 162, 235, 0.2)",
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
          text: "Pressure (hPa)",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default PressureChart;
