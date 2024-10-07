import React, { useState, useEffect } from "react";
import Button from "./common/Button";
import VisualizeData from "./VisualizeData";

const SelectData = ({ planet, event, nonEvent }) => {
  const [chartData, setChartData] = useState({
    pressureData: [],
    temperatureData: [],
    seisData: [],
    noiseData: [],
    eventData: [],
  });

  const [clickedBtn, setClickedBtn] = useState("1");
  const [date, setDate] = useState("");

  useEffect(() => {
    // planet에 따라 초기 date 값을 설정
    if (planet === "Mars") {
      setDate("January 10th, 2024"); // Mars의 경우
    } else if (planet === "Earth") {
      setDate("June 15th, 2024"); // Earth의 경우 (원하는 초기값으로 변경)
    }
  }, [planet]);

  const btnHandler = (id) => {
    setClickedBtn(id);
    fetchData(id);
  };

  const fetchData = async (caseId) => {
    // 서버 대신 더미 데이터를 설정합니다.
    // const dummyData = {
    //   pressureData: [
    //     1,2,3
    //   ],
    //   temperatureData: [
    //     1,2,3
    //   ],
    //   seisData: [
    //     1,2,3
    //   ],
    //   noiseData: [
    //     1,2,3
    //   ],
    //   eventData: [
    //     1,2,3
    //   ],
    // };

    // 서버에서 데이터를 가져오는 코드
    const response = await fetch(`http://220.68.27.140:8000/getinfo?planet=${planet}&case=${caseId}`);
    const data = await response.json();
    
    // 서버에서 받은 데이터 : ({pressure: [], temperature: [], seis: [], noise: [], event: []})
    // 서버에서 받은 데이터를 chartData 상태에 설정합니다.
    setChartData({
      pressureData: data.pressure,
      temperatureData: data.temperature,
      seisData: data.seis,
      noiseData: data.noise,
      eventData: data.event,
    });


    // 더미 데이터를 chartData 상태에 설정합니다.
    // setChartData(dummyData);
  };

  const formatDate = (dateString) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    const date = new Date(dateString);
    const formattedDate = date.toLocaleDateString("en-US", options);
    return formattedDate.replace(/(\d+)(?=,)/, "$1th");
  };

  useEffect(() => {
    fetchData(clickedBtn);
  }, [clickedBtn]);

  return (
    <div>
      <div
        className="h-[313px] rounded-3xl"
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
          <div className="pt-[42px] pretendard text-[#FFFFFF] text-[24px] font-bold leading-[28.8px] tracking-[-0.02em]">
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
      <VisualizeData
        windData={chartData.temperatureData}  // 더미 데이터 사용
        pressureData={chartData.pressureData}  
        seisData={chartData.seisData} 
        noiseData={chartData.noiseData} 
        eventData={chartData.eventData}  // 더미 데이터 사용
      />
    </div>
  );
};

export default SelectData;