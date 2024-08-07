import { useEffect } from "react";
import { useData } from "./store";

export const MainView = () => {
  const { data, getData } = useData();
  console.log(data);

  useEffect(() => {
    getData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col w-screen min-h-screen bg-black">
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
      <div className="flex">
        <div className="flex flex-col flex-1 gap-8 p-8">
          <div className="flex flex-col gap-2">
            <div className="text-white">Question</div>
            <div
              className="flex flex-col border rounded-lg"
              style={{ borderColor: "#454545", backgroundColor: "#1a1a1a" }}
            >
              <div className="p-5">
                <textarea className="w-full resize-none"></textarea>
              </div>
              <div className="flex justify-end p-5">
                <button className="px-5 py-2 text-black bg-white rounded-lg">
                  Solve
                </button>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div className="text-white">Specifications</div>
            <div
              className="flex flex-col rounded-lg"
              style={{ background: "#1f1f1f" }}
            >
              <div className="flex">
                <div
                  className="flex flex-col gap-3 p-5"
                  style={{ flex: 3, color: "white" }}
                >
                  <div className="" style={{ color: "#ededed" }}>
                    This recipe is designed to achieve a higher SiO etch rate
                    while maintaining good selectivity over the PR mask and
                    minimizing polymer redeposition.
                  </div>
                  <ul className="pl-4 list-disc">
                    <li>
                      Gases:
                      <ul className="pl-4 list-disc">
                        <li>CF4: 50 sccm</li>
                        <li>CHF3: 20 sccm</li>
                        <li>Ar: 10 sccm</li>
                      </ul>
                    </li>
                    <li>ICP Power: 800 W</li>
                    <li>Bias Power: 100 W</li>
                    <li>Temperature: 20°C</li>
                  </ul>
                </div>
                <div
                  className="flex flex-col justify-center gap-3 p-5"
                  style={{ flex: 2, backgroundColor: "#2e2e2e" }}
                >
                  <img src="/public/images/image-14.png" />
                </div>
              </div>
              <div className="flex justify-end p-5">
                <button
                  className="px-5 py-2 text-black bg-white rounded-lg"
                  style={{ backgroundColor: "white", color: "black" }}
                >
                  Suggest Params
                </button>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div className="text-white">Plans</div>
            <div
              className="flex flex-col border rounded-lg"
              style={{ borderColor: "#454545", backgroundColor: "#1a1a1a" }}
            >
              <div className="flex items-center gap-2 p-5">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <g clipPath="url(#clip0_14399_59232)">
                    <path
                      d="M4.9987 8.00016L6.9987 10.0002L10.9987 6.00016M14.6654 8.00016C14.6654 11.6821 11.6806 14.6668 7.9987 14.6668C4.3168 14.6668 1.33203 11.6821 1.33203 8.00016C1.33203 4.31826 4.3168 1.3335 7.9987 1.3335C11.6806 1.3335 14.6654 4.31826 14.6654 8.00016Z"
                      stroke="#58C760"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_14399_59232">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>
                <div>
                  <span className="text-white font-500">Main task:</span>
                  <span style={{ color: "#a1a1a1", paddingLeft: "2px" }}>
                    sit amet consectetur
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2 p-5 px-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <g clipPath="url(#clip0_14399_59232)">
                    <path
                      d="M4.9987 8.00016L6.9987 10.0002L10.9987 6.00016M14.6654 8.00016C14.6654 11.6821 11.6806 14.6668 7.9987 14.6668C4.3168 14.6668 1.33203 11.6821 1.33203 8.00016C1.33203 4.31826 4.3168 1.3335 7.9987 1.3335C11.6806 1.3335 14.6654 4.31826 14.6654 8.00016Z"
                      stroke="#58C760"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_14399_59232">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>
                <div>
                  <span className="text-white font-500">Subtask 1:</span>
                  <span style={{ color: "#a1a1a1", paddingLeft: "2px" }}>
                    sit amet consectetur
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2 p-5 px-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <g clipPath="url(#clip0_14399_59232)">
                    <path
                      d="M4.9987 8.00016L6.9987 10.0002L10.9987 6.00016M14.6654 8.00016C14.6654 11.6821 11.6806 14.6668 7.9987 14.6668C4.3168 14.6668 1.33203 11.6821 1.33203 8.00016C1.33203 4.31826 4.3168 1.3335 7.9987 1.3335C11.6806 1.3335 14.6654 4.31826 14.6654 8.00016Z"
                      stroke="#58C760"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_14399_59232">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>
                <div>
                  <span className="text-white font-500">Subtask 2:</span>
                  <span style={{ color: "#a1a1a1", paddingLeft: "2px" }}>
                    sit amet consectetur
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2 p-5 px-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <g clipPath="url(#clip0_14399_59232)">
                    <path
                      d="M4.9987 8.00016L6.9987 10.0002L10.9987 6.00016M14.6654 8.00016C14.6654 11.6821 11.6806 14.6668 7.9987 14.6668C4.3168 14.6668 1.33203 11.6821 1.33203 8.00016C1.33203 4.31826 4.3168 1.3335 7.9987 1.3335C11.6806 1.3335 14.6654 4.31826 14.6654 8.00016Z"
                      stroke="#58C760"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_14399_59232">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>
                <div>
                  <span className="text-white font-500">Subtask 3:</span>
                  <span style={{ color: "#a1a1a1", paddingLeft: "2px" }}>
                    sit amet consectetur
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2 p-5 px-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <g clipPath="url(#clip0_14399_59232)">
                    <path
                      d="M4.9987 8.00016L6.9987 10.0002L10.9987 6.00016M14.6654 8.00016C14.6654 11.6821 11.6806 14.6668 7.9987 14.6668C4.3168 14.6668 1.33203 11.6821 1.33203 8.00016C1.33203 4.31826 4.3168 1.3335 7.9987 1.3335C11.6806 1.3335 14.6654 4.31826 14.6654 8.00016Z"
                      stroke="#58C760"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_14399_59232">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>
                <div>
                  <span className="text-white font-500">Subtask 4:</span>
                  <span style={{ color: "#a1a1a1", paddingLeft: 2 }}>
                    sit amet consectetur
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          className="flex flex-col flex-1 gap-8 p-8 border-l"
          style={{ borderColor: "#252525" }}
        >
          <div className="flex flex-col gap-2">
            <div className="text-white">Solution</div>
            <div
              className="flex flex-col rounded-lg"
              style={{ background: "#1f1f1f", border: "1px solid #272626" }}
            >
              <div
                className="flex items-center justify-between p-5 rounded-t-lg"
                style={{ background: "#292929" }}
              >
                <div className="font-medium text-white">
                  First suggested parameter
                </div>
                <div
                  className="px-4 py-2 text-xs rounded-full"
                  style={{ backgroundColor: "#00320b", color: "#00ca51" }}
                >
                  Recommended
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className=" px-6 py-2.5 font-medium" style={{ flex: 2 }}>
                  Parameter
                </div>
                <div className=" px-6 py-2.5 font-medium" style={{ flex: 3 }}>
                  Value
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Ar (Argon)
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Power
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  123231 W
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  DCS (Dichlorosilane)
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Temperature
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  123231 W
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Pressure
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div
              className="flex flex-col rounded-lg"
              style={{
                background: "#1f1f1f",
                border: "1px solid #272626",
                opacity: 0.6,
              }}
            >
              <div
                className="flex items-center justify-between p-5 rounded-t-lg"
                style={{ background: "#292929" }}
              >
                <div className="font-medium text-white">
                  Second suggested parameter
                </div>
                <div
                  className="px-4 py-2 text-xs rounded-full"
                  style={{ backgroundColor: "#00320b", color: "#00ca51" }}
                >
                  Recommended
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className=" px-6 py-2.5 font-medium" style={{ flex: 2 }}>
                  Parameter
                </div>
                <div className=" px-6 py-2.5 font-medium" style={{ flex: 3 }}>
                  Value
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Ar (Argon)
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Power
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  123231 W
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  DCS (Dichlorosilane)
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
              <div
                className="flex text-white"
                style={{ backgroundColor: "#0f0f0f" }}
              >
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Temperature
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  123231 W
                </div>
              </div>
              <div className="flex text-white">
                <div className="px-6 py-2.5" style={{ flex: 2 }}>
                  Pressure
                </div>
                <div className="px-6 py-2.5" style={{ flex: 3 }}>
                  1213 sccm
                </div>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div className="text-white">
              Steps to Optimize the Etching Process
            </div>
            <div>
              <img className="w-full" src="/public/images/image-16.png" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
