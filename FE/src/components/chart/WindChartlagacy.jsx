// WindChart.jsx
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
import { RealTimeScale, StreamingPlugin } from "chartjs-plugin-streaming";
import "chartjs-adapter-luxon";

ChartJS.register(
  StreamingPlugin,
  RealTimeScale,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const WindChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.time),
    datasets: [
      {
        label: "Temperature (°C)",
        data: data,
        borderColor: "rgba(255, 99, 132, 1)", // 빨간색
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        pointRadius: 1, // 점의 크기 조정
        fill: true,
        yAxisID: "y1",
      },
      {
        label: "Pressure (hPa)",
        data: data.map((item) => item.pressure),
        borderColor: "rgba(54, 162, 235, 1)", // 파란색
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        pointRadius: 1, // 점의 크기 조정
        fill: true,
        yAxisID: "y2",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: false,
        text: "Temperature and Pressure",
      },
    },
    scales: {
      x: {
        type: "realtime",
        display: false, // x축 숨기기
        realtime: {
          delay: 2000,
          onRefresh: (chart) => {
            chart.data.datasets.forEach((dataset) => {
              dataset.data.push({
                x: Date.now(),
                y: Math.random(),
              });
            });
          },
        },
      },
      y1: {
        type: "linear",
        position: "left",
        title: {
          display: true,
          text: "Temperature (°C)",
        },
      },
      y2: {
        type: "linear",
        position: "right",
        title: {
          display: true,
          text: "Pressure (hPa)",
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default WindChart;
