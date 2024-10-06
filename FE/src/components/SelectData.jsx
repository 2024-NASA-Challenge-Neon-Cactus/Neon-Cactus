import React from "react";
import Button from "./common/Button";
import VisualizeData from "./VisualizeData";

const SelectData = ({ planet, event, nonEvent }) => {
  return (
    <div>
      <div className=" h-[313px] border border-[#999999] rounded-3xl  backdrop-blur-3xl ">
        <div className="pl-[48px]">
          <div className="pt-[42px]  pretendard text-[#FFFFFF] text-[24px] font-bold leading-[28.8px] tracking-[-0.02em]">
            October 10th, 2024
          </div>
          <div className="pt-[7px] d-din font-bold text-[72px] tracking-[-0.02em] leading-[78.19px] text-[#FFFFFF]">
            {planet}
          </div>
          <div className="flex flex-row pt-[23px] justify-between pr-[82px]">
            <div className="w-[408px]">
              <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium">
                {event}
              </div>
              <div className="pt-[16px] flex items-center justify-between">
                <Button btn="Case 1" />
                <Button btn="Case 2" />
                <Button btn="Case 3" />
              </div>
            </div>
            <div className="w-[408px]">
              <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium">
                {nonEvent}
              </div>
              <div className="pt-[16px] flex items-center justify-between">
                <Button btn="Case 1" />
                <Button btn="Case 2" />
                <Button btn="Case 3" />
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
