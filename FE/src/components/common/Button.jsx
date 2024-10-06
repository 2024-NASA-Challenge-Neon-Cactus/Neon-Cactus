import React from "react";

const Button = ({ btn, onClick, isClicked }) => {
  return (
    <>
      <button
        onClick={onClick}
        className={`w-[120px] h-[52px] border rounded-lg text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 items-center ${
          isClicked
            ? "font-bold border-[#F64137] bg-[#F64137]"
            : "font-medium border-[#FFFFFF]"
        }`}
      >
        {btn}
      </button>
    </>
  );
};

export default Button;
