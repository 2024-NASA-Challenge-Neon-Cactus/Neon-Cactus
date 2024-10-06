import React from "react";
import WindChart from "../components/chart/WindChart";

const VisualizeData = () => {
  const pressureAndTemperatureData = [
    { time: "2024-10-01T00:00:00Z", pressure: 1012, temperature: 15 },
    { time: "2024-10-01T01:00:00Z", pressure: 1011, temperature: 14.5 },
    { time: "2024-10-01T02:00:00Z", pressure: 1013, temperature: 15.2 },
    { time: "2024-10-01T03:00:00Z", pressure: 1010, temperature: 14.8 },
    { time: "2024-10-01T04:00:00Z", pressure: 1012, temperature: 15.0 },
    { time: "2024-10-01T05:00:00Z", pressure: 1011, temperature: 15.1 },
    { time: "2024-10-01T06:00:00Z", pressure: 1013, temperature: 14.7 },
    { time: "2024-10-01T07:00:00Z", pressure: 1014, temperature: 15.4 },
    { time: "2024-10-01T08:00:00Z", pressure: 1012, temperature: 15.6 },
    { time: "2024-10-01T09:00:00Z", pressure: 1010, temperature: 15.2 },
    { time: "2024-10-01T10:00:00Z", pressure: 1009, temperature: 15.8 },
    { time: "2024-10-01T11:00:00Z", pressure: 1011, temperature: 16.0 },
    { time: "2024-10-01T12:00:00Z", pressure: 1013, temperature: 16.2 },
    { time: "2024-10-01T13:00:00Z", pressure: 1012, temperature: 16.5 },
    { time: "2024-10-01T14:00:00Z", pressure: 1011, temperature: 16.7 },
    { time: "2024-10-01T15:00:00Z", pressure: 1010, temperature: 16.3 },
    { time: "2024-10-01T16:00:00Z", pressure: 1008, temperature: 16.1 },
    { time: "2024-10-01T17:00:00Z", pressure: 1010, temperature: 15.9 },
    { time: "2024-10-01T18:00:00Z", pressure: 1011, temperature: 15.5 },
    { time: "2024-10-01T19:00:00Z", pressure: 1013, temperature: 15.3 },
    { time: "2024-10-01T20:00:00Z", pressure: 1012, temperature: 15.4 },
    { time: "2024-10-01T21:00:00Z", pressure: 1011, temperature: 15.6 },
    { time: "2024-10-01T22:00:00Z", pressure: 1010, temperature: 15.7 },
    { time: "2024-10-01T23:00:00Z", pressure: 1009, temperature: 15.8 },
  ];

  return (
    <div
      className=" h-[635px] mt-[10px] border-[#999999] rounded-3xl p-[30px] flex flex-row"
      style={{
        backdropFilter: "blur(80px)",
        border: "1px solid",
        borderImageSource:
          "linear-gradient(160.8deg, rgba(255, 255, 255, 0.6) -28.98%, rgba(153, 153, 153, 0.6) 75.6%)",
        backgroundColor: "#FFFFFF1A",
      }}
    >
      <div className="w-[442px] h-full mr-[84px]">
        <div
          className="h-[223px] border-t-[1px] border-[#CBCBCB66] mb-[93px]"
          alt="Wind Speed and Temperature"
        >
          <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium pt-[10px]">
            Wind Speed and Temperature
          </div>
          <div className="text-[#FFFFFF] text-[16px] tracking-[-0.02em] leading-[19.2px] pt-[6px]">
            (TWINS Sensor)
          </div>
          <div className="mt-[20px]">
            <WindChart data={pressureAndTemperatureData} />
          </div>
        </div>
        <div
          className="h-[223px] border-t-[1px] border-[#CBCBCB66]"
          alt="Pressure"
        >
          <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium  pt-[10px]">
            Pressure
          </div>
          <div className="text-[#FFFFFF] text-[16px] tracking-[-0.02em] leading-[19.2px] pt-[6px]">
            (Pressure Sensor)
          </div>
        </div>
      </div>
      <div className="w-[442px] h-full ">
        <div
          className="h-[164px] border-t-[1px] border-[#CBCBCB66]"
          alt="VBB Z"
        >
          <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium pt-[10px]">
            VBB Z
          </div>
        </div>
        <div
          className="h-[164px] border-t-[1px] border-[#CBCBCB66] my-[20px]"
          alt="Noise Waveforms"
        >
          <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium pt-[10px]">
            Noise Waveforms
          </div>
        </div>
        <div
          className="h-[164px] border-t-[1px] border-[#CBCBCB66]"
          alt="Event Waveforms"
        >
          <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium pt-[10px]">
            Event Waveforms
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualizeData;
