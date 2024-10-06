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

const EventChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index + 1), // 인덱스를 라벨로 사용
    datasets: [
      {
        label: "Event Intensity",
        data: data,
        borderColor: "rgba(255, 206, 86, 1)", // 노란색
        backgroundColor: "rgba(255, 206, 86, 0.2)",
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
          text: "Event Intensity",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default EventChart;
