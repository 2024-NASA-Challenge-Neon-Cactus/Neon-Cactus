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

const SeisChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index + 1), // 인덱스를 라벨로 사용
    datasets: [
      {
        label: "Seismic Activity",
        data: data,
        borderColor: "rgba(75, 192, 192, 1)", // 청록색
        backgroundColor: "rgba(75, 192, 192, 0.2)",
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
          text: "Seismic Intensity",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default SeisChart;
