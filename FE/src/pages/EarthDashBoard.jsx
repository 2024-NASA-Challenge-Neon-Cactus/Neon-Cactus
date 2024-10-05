import React from "react";
import Planet from "../components/Planet";
import SelectData from "../components/SelectData";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import VisualizeData from "../components/VisualizeData";
const EarthDashBoard = () => {
  return (
    <div>
      <div className="w-screen bg-black ">
        <div className="relative w-full h-full items-center flex">
          <div className=" w-[900px] h-[900px] z-0">
            <Canvas camera={{ position: [0, 0, 15], fov: 75 }}>
              <ambientLight intensity={0.5} />
              <OrbitControls target={[0, 0, 0]} />
              <Planet planet="earth" />
            </Canvas>
          </div>
          <div className="flex flex-col w-[1064px] ml-[-100px] my-[56px] mr-[70px] z-10">
            <SelectData
              planet="Earth"
              event="Earthquakes"
              nonEvent="Non-event"
            />
            <VisualizeData />
          </div>
        </div>
      </div>
    </div>
  );
};

export default EarthDashBoard;
