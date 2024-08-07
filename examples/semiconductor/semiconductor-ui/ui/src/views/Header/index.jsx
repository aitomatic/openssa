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
