import React from "react";

const VisualizeData = () => {
  return (
    <div className=" h-[635px] mt-[19px] border border-[#999999] rounded-3xl  backdrop-blur-3xl">
      <div className="p-[48px] flex flex-row ">
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
    </div>
  );
};

export default VisualizeData;
