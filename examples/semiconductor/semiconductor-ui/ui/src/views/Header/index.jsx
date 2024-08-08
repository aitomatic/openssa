export const Header = () => {
  return (
    <div className="flex px-2.5 py-6 justify-center gap-6 border-b border-gray-200 bg-black text-white">
      <div className="flex flex-col gap-3 items-center after:content-[''] step-item">
        <div className="flex w-4 h-4 rounded-full bg-[#00ca51]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
          >
            <path
              d="M13.3346 4L6.0013 11.3333L2.66797 8"
              stroke="black"
              strokeWidth="1.33333"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="flex flex-col items-center gap-1">
          <div>Specifications</div>
          <div>Loremm ipsum dolor sit amet consectetur</div>
        </div>
      </div>
      <div className="flex flex-col items-center gap-3">
        <div className="flex w-4 h-4 rounded-full bg-[#00ca51]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
          >
            <path
              d="M13.3346 4L6.0013 11.3333L2.66797 8"
              stroke="black"
              strokeWidth="1.33333"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="flex flex-col items-center gap-1">
          <div>Paramters</div>
          <div>Loremm ipsum dolor sit amet consectetur</div>
        </div>
      </div>
      <div className="flex flex-col items-center gap-3">
        <div className="flex w-4 h-4 rounded-full bg-[#00ca51]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
          >
            <path
              d="M13.3346 4L6.0013 11.3333L2.66797 8"
              stroke="black"
              strokeWidth="1.33333"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="flex flex-col items-center gap-1">
          <div>Steps</div>
          <div>Loremm ipsum dolor sit amet consectetur</div>
        </div>
      </div>
    </div>
  );
};

export const TitleHeader = () => {
  return (
    <div className="flex gap-4 p-8 border-b border-[#2E2E2E]">
      <div
        className="p-1.5 h-[60px] flex items-center justify-center w-15 border-2 rounded-xl border-[#FFFFFF1F]"
        style={{
          background:
            "linear-gradient(178deg, rgba(255, 255, 255, 0.00)2%, rgba(255, 255, 255, 0.12)98.17%)",
        }}
      >
        <svg
          width="43"
          height="43"
          viewBox="0 0 43 43"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g filter="url(#filter0_d_14481_1935)">
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M3.17969 19C14.6208 19 21.1797 12.4411 21.1797 1C21.1797 12.4411 27.7386 19 39.1797 19C27.7386 19 21.1797 25.5589 21.1797 37C21.1797 25.5589 14.6208 19 3.17969 19Z"
              fill="url(#paint0_linear_14481_1935)"
            />
          </g>
          <defs>
            <filter
              id="filter0_d_14481_1935"
              x="0.179688"
              y="0.25"
              width="42"
              height="42"
              filterUnits="userSpaceOnUse"
              colorInterpolationFilters="sRGB"
            >
              <feFlood floodOpacity="0" result="BackgroundImageFix" />
              <feColorMatrix
                in="SourceAlpha"
                type="matrix"
                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                result="hardAlpha"
              />
              <feMorphology
                radius="1.5"
                operator="erode"
                in="SourceAlpha"
                result="effect1_dropShadow_14481_1935"
              />
              <feOffset dy="2.25" />
              <feGaussianBlur stdDeviation="2.25" />
              <feComposite in2="hardAlpha" operator="out" />
              <feColorMatrix
                type="matrix"
                values="0 0 0 0 0.141176 0 0 0 0 0.141176 0 0 0 0 0.141176 0 0 0 0.1 0"
              />
              <feBlend
                mode="normal"
                in2="BackgroundImageFix"
                result="effect1_dropShadow_14481_1935"
              />
              <feBlend
                mode="normal"
                in="SourceGraphic"
                in2="effect1_dropShadow_14481_1935"
                result="shape"
              />
            </filter>
            <linearGradient
              id="paint0_linear_14481_1935"
              x1="21.1797"
              y1="1"
              x2="21.1797"
              y2="37"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="white" stopOpacity="0.8" />
              <stop offset="1" stopColor="white" stopOpacity="0.5" />
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div className="flex flex-col">
        <div className="text-[24px] text-[#EDEDED] font-semibold">
          SiO2 Etching Advisor
        </div>
        <div className="text-[#DCDCDC] text-[20px]">powered by SemiKong</div>
      </div>
    </div>
  );
};
