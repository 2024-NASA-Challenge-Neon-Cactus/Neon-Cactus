import React from "react";
import Planet from "../components/Planet";
import SelectData from "../components/SelectData";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import VisualizeData from "../components/VisualizeData";
import chevron from "../assets/icons/chevron.svg";

const MarsDashBoard = () => {
  return (
    <div>
      <div className="w-screen h-[120vh] bg-black ">
        <div className="relative w-full h-full flex">
          <div className=" w-[900px] h-[900px] mt-[90px] z-0">
            <div className="relative flex flex-row  ml-[70px] mt-[-34px]">
              <img src={chevron} className="w-[24px] h-[24px]"></img>
              <button className="text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-bold">
                Back
              </button>
            </div>
            <Canvas camera={{ position: [0, 0, 15], fov: 75 }}>
              <ambientLight intensity={0.5} />
              <OrbitControls target={[0, 0, 0]} />
              <Planet planet="mars" />
            </Canvas>
          </div>
          <div className="flex flex-col w-[1064px] ml-[-130px] my-[56px] mr-[70px] z-10">
            <SelectData
              planet="Mars"
              event="Seismic Event"
              nonEvent="Non-event"
            />
            {/* <VisualizeData /> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarsDashBoard;
