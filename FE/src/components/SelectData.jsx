import React, { useState, useEffect } from "react";
import Button from "./common/Button";
import VisualizeData from "./VisualizeData";

const SelectData = ({ planet, event, nonEvent }) => {
  const [clickedBtn, setClickedBtn] = useState("1");
  const [date, setDate] = useState("");

  useEffect(() => {
    // planet에 따라 초기 date 값을 설정
    if (planet === "Mars") {
      setDate("January 10th, 2024"); // Mars의 경우
    } else if (planet === "Earth") {
      setDate("June 15th, 2024"); // Earth의 경우 (원하는 초기값으로 변경)
    }
  }, [planet]); // planet이 변경될 때마다 effect 실행

  const btnHandler = (id) => {
    setClickedBtn(id);
    fetchData(id);
  };

  const fetchData = async (caseId) => {
    try {
      const response = await fetch(
        `http://220.68.27.140:8000/getinfo/?planet=${planet}&case=${caseId}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setDate(formatDate(data.date)); // API에서 받은 날짜를 사용하여 상태를 업데이트합니다.
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const formatDate = (dateString) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    const date = new Date(dateString);
    const formattedDate = date.toLocaleDateString("en-US", options);

    // "June 15, 2024"에서 "June 15th, 2024"로 변경
    return formattedDate.replace(/(\d+)(?=,)/, "$1th");
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
            {date}
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
                  onClick={() => btnHandler("1")}
                  isClicked={clickedBtn === "1"}
                />
                <Button
                  btn="Case 2"
                  onClick={() => btnHandler("2")}
                  isClicked={clickedBtn === "2"}
                />
                <Button
                  btn="Case 3"
                  onClick={() => btnHandler("3")}
                  isClicked={clickedBtn === "3"}
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
                  onClick={() => btnHandler("4")}
                  isClicked={clickedBtn === "4"}
                />
                <Button
                  btn="Case 2"
                  onClick={() => btnHandler("5")}
                  isClicked={clickedBtn === "5"}
                />
                <Button
                  btn="Case 3"
                  onClick={() => btnHandler("6")}
                  isClicked={clickedBtn === "6"}
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
