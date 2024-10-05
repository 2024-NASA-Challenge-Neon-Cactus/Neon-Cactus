import React from "react";
import Button from "./common/Button";
import VisualizeData from "./VisualizeData";

const SelectData = ({ planet, event, nonEvent }) => {
  return (
    <div>
      <div className=" h-[277px] border border-[#999999] rounded-3xl  backdrop-blur-3xl ">
        <div className="pl-[48px]">
          <div className="pt-[20px] pretendard text-[#FFFFFF] text-[24px] font-bold leading-[28.8px] tracking-[-0.02em]">
            October 10th, 2024
          </div>
          <div className="pt-[7px] d-din font-bold text-[72px] tracking-[-0.02em] leading-[78.19px] text-[#FFFFFF]">
            {planet}
          </div>
          <div className="flex flex-row pt-[20px] justify-between pr-[82px]">
            <div className="w-[408px]">
              <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium">
                {event}
              </div>
              <div className="pt-[16px] flex items-center justify-between">
                <Button />
                <Button />
                <Button />
              </div>
            </div>
            <div className="w-[408px]">
              <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium">
                {nonEvent}
              </div>
              <div className="pt-[16px] flex items-center justify-between">
                <Button />
                <Button />
                <Button />
              </div>
            </div>
          </div>
        </div>
      </div>
      <VisualizeData />
    </div>
  );
};

export default SelectData;
