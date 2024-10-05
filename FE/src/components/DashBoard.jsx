import { OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React from "react";
import Mars from "./planets/Mars";
import SelectData from "./SelectData";
import VisualizeData from "./VisualizeData";

const DashBoard = () => {
  return (
    <div className="w-screen bg-black ">
      <div className="relative w-full h-full items-center flex">
        <div className=" w-[900px] h-[900px] z-0">
          <Canvas camera={{ position: [0, 0, 15], fov: 75 }}>
            <ambientLight intensity={0.5} />
            <OrbitControls target={[0, 0, 0]} />
            <Mars position={[0, 0, 0]} />
          </Canvas>
        </div>
        <div className="flex flex-col w-[1064px] ml-[-100px] my-[56px] mr-[70px] z-10">
          <SelectData />
          <VisualizeData />
        </div>
      </div>
    </div>
  );
};

export default DashBoard;
