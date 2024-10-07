import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Planet from "../components/Planet";
import { Canvas } from "@react-three/fiber";

const MainPage = () => {
  const navigate = useNavigate();
  const [clickedBtn, setClickedBtn] = useState(null); // 클릭된 버튼 ID 상태

  const handleButtonClick = (id) => {
    setClickedBtn(clickedBtn === id ? null : id);
    if (id === "earthquake") {
      navigate("/earthquake");
    } else if (id === "marsquake") {
      navigate("/marsquake");
    }
  };

  return (
    <div className="bg-black w-screen h-screen items-center justify-center text-center">
      <div className="pt-[156px] d-din font-bold text-[72px] tracking-[-0.02em] leading-[78.19px] text-[#FFFFFF]">
        <span className="text-[#FFFFFF]">Symphony of</span>
        <span className="text-[#F64137]"> Seismics</span>
      </div>
      <div className="pt-[28px] relative flex flex-row items-center justify-center">
        <div className="w-5 h-5 bg-[#F64137]"></div>
        <div className="pretendard text-[#FFFFFF] text-[24px] font-bold leading-[28.8px] tracking-[-0.02em] px-[14px]">
          Extracting the Rhythms of Earth's and Mars' Seismic Data, No Noise!
        </div>
        <div className="w-5 h-5 bg-[#F64137]"></div>
      </div>
      <div className="mx-auto w-[1136px] pretendard text-[#FFFFFF] text-[17px] leading-[36px] tracking-[-0.02em] pt-[57px] pb-[114px] text-center">
        Welcome to our Seismic of Symphony! Explore the dynamic worlds of Earth
        and Mars through the lens of seismic data. Our web app brings together
        the unique rhythms of planetary quakes, uncovering the secrets beneath
        their surfaces. Join us on this scientific journey as we harmonize
        Earth’s tremors with Mars’ mysteries, revealing insights into the forces
        that shape these worlds.
      </div>

      <div className="flex justify-center">
        <button
          onClick={() => handleButtonClick("earthquake")} // 클릭 시 버튼 ID 전달
          className={`w-[197px] h-[52px] border rounded-lg text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 items-center ${
            clickedBtn === "earthquake"
              ? "font-bold border-[#F64137] bg-[#F64137]"
              : "font-medium border-[#FFFFFF]"
          } mr-[200px]`}
        >
          View Earthquake
        </button>
        <button
          onClick={() => handleButtonClick("marsquake")} // 클릭 시 버튼 ID 전달
          className={`w-[197px] h-[52px] border rounded-lg text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 items-center ${
            clickedBtn === "marsquake"
              ? "font-bold border-[#F64137] bg-[#F64137]"
              : "font-medium border-[#FFFFFF]"
          }`}
        >
          View Marsquake
        </button>
      </div>

      <div className="relative flex flex-row w-[800px] h-[350px] justify-center items-center mx-auto">
        <Canvas className="">
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Planet planet="earth" scale={[0.03, 0.03, 0.03]} />
        </Canvas>

        <Canvas className="">
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Planet planet="mars" scale={[0.03, 0.03, 0.03]} />
        </Canvas>
      </div>
    </div>
  );
};

export default MainPage;
