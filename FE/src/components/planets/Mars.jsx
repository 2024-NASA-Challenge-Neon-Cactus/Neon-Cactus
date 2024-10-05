import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import React, { useRef } from "react";
import { TextureLoader } from "three"; // 필요한 three.js 클래스만 임포트
import marsTexturePath from "../../assets/images/mars.jpg"; // 텍스처 경로

const Mars = () => {
  const marsRef = useRef();
  const marsTexture = useLoader(TextureLoader, marsTexturePath); // TextureLoader 사용

  useFrame(() => {
    if (marsRef.current) {
      marsRef.current.rotation.x += 0.0001;
      marsRef.current.rotation.y += 0.0005;
      marsRef.current.rotation.z += 0.0001;
    }
  });

  return (
    <mesh ref={marsRef} scale={[0.1, 0.1, 0.1]}>
      <sphereGeometry args={[80, 64, 32]} />
      <meshBasicMaterial map={marsTexture} />
    </mesh>
  );
};

export default Mars;
