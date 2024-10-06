import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import React, { useRef } from "react";
import { TextureLoader } from "three";
import marsTexturePath from "../assets/images/mars.jpg";
import earthTexturePath from "../assets/images/earth.jpg";

const Planet = ({ planet }) => {
  const planetRef = useRef();
  const planetTexture = useLoader(
    TextureLoader,
    planet === "mars" ? marsTexturePath : earthTexturePath
  );

  useFrame(() => {
    if (planetRef.current) {
      planetRef.current.rotation.x += 0.0001;
      planetRef.current.rotation.y += 0.0005;
      planetRef.current.rotation.z += 0.0001;
    }
  });

  return (
    <mesh ref={planetRef} scale={[0.1, 0.1, 0.1]}>
      <sphereGeometry args={[80, 64, 32]} />
      <meshBasicMaterial map={planetTexture} />
    </mesh>
  );
};

export default Planet;
