import React from "react";
import WindChart from "../components/chart/WindChart";
import PressureChart from "../components/chart/PressureChart";
import SeisChart from "../components/chart/SeisChart";
import NoiseChart from "../components/chart/NoiseChart";
import EventChart from "../components/chart/EventChart";

const VisualizeData = ({ windData, pressureData, seisData, noiseData, eventData }) => {
  return (
    <div
      className="relative mt-[10px] border-[#999999] rounded-3xl p-[30px] flex flex-row"
      style={{
        backdropFilter: "blur(80px)",
        border: "1px solid",
        borderImageSource:
          "linear-gradient(160.8deg, rgba(255, 255, 255, 0.6) -28.98%, rgba(153, 153, 153, 0.6) 75.6%)",
        backgroundColor: "#FFFFFF1A",
      }}
    >
      <div className="w-[442px] h-full mr-[84px]">
        <div className="h-[223px] border-t-[1px] border-[#CBCBCB] mt-4">
          <WindChart data={windData} />
        </div>
        <div className="h-[223px] border-t-[1px] border-[#CBCBCB] mt-4">
          <PressureChart data={pressureData} />
        </div>
      </div>
      <div className="w-[442px] h-full">
        <div className="h-[223px] border-t-[1px] border-[#CBCBCB] mt-4">
          <SeisChart data={seisData} />
        </div>
        <div className="h-[223px] border-t-[1px] border-[#CBCBCB] mt-4">
          <NoiseChart data={noiseData} />
        </div>
        <div className="h-[223px] border-t-[1px] border-[#CBCBCB] mt-4">
          <EventChart data={eventData} />
        </div>
      </div>
    </div>
  );
};

export default VisualizeData;
