import React from "react";

const Button = ({ btn }) => {
  return (
    <>
      <button className="w-[120px] h-[52px] border border-[#FFFFFF] rounded-lg text-[#FFFFFF] text-[20px] tracking-[-0.02em] leading-6 font-medium items-center">
        {btn}
      </button>
    </>
  );
};

export default Button;
