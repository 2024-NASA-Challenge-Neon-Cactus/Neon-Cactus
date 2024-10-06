import React, { useState } from "react";
import Button from "./common/Button";
import VisualizeData from "./VisualizeData";
import { useAnimations } from "@react-three/drei";

const SelectData = ({ planet, event, nonEvent }) => {
  const [clickedBtn, setClickedBtn] = useState("case1");

  const btnHandler = (id) => {
    setClickedBtn(id);
  };

  return (
    <div>
      <div
        className=" h-[313px] rounded-3xl "
        style={{
          backdropFilter: "blur(80px)",
          border: "1px solid",
          borderColor: "#CBCBCB66",
          borderImageSource:
            "linear-gradient(160.8deg, rgba(255, 255, 255, 0.6) -28.98%, rgba(153, 153, 153, 0.6) 75.6%)",
          backgroundColor: "#FFFFFF1A",
        }}
      >
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
                <Button
                  btn="Case 1"
                  onClick={() => btnHandler("case1")}
                  isClicked={clickedBtn === "case1"}
                />
                <Button
                  btn="Case 2"
                  onClick={() => btnHandler("case2")}
                  isClicked={clickedBtn === "case2"}
                />
                <Button
                  btn="Case 3"
                  onClick={() => btnHandler("case3")}
                  isClicked={clickedBtn === "case3"}
                />
              </div>
            </div>
            <div className="w-[408px]">
              <div className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium">
                {nonEvent}
              </div>
              <div className="pt-[16px] flex items-center justify-between">
                <Button
                  btn="Case 1"
                  onClick={() => btnHandler("noncase1")}
                  isClicked={clickedBtn === "noncase1"}
                />
                <Button
                  btn="Case 2"
                  onClick={() => btnHandler("noncase2")}
                  isClicked={clickedBtn === "noncase2"}
                />
                <Button
                  btn="Case 3"
                  onClick={() => btnHandler("noncase3")}
                  isClicked={clickedBtn === "noncase3"}
                />
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
