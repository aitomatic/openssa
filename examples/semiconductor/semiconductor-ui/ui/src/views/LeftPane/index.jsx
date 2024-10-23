import { useState } from "react";
import { useData } from "../store";
import { MarkdownViewer } from "../components/MarkdownViewer";

export const Specification = () => {
  return (
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
              This recipe is designed to achieve a higher SiO etch rate while
              maintaining good selectivity over the PR mask and minimizing
              polymer redeposition.
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
  );
};

export const Plan = () => {
  return (
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
  );
};

export const Data1 = () => {
  const { data } = useData();
  const { recipe_1 } = data;
  if (!recipe_1) return <></>;
  const strings = recipe_1.split("\n");

  return (
    <div className="flex flex-col h-full gap-2">
      <div
        className="flex flex-col rounded-lg"
        style={{ background: "#1f1f1f" }}
      >
        <div className="text-white  p-4 bg-[#292929] rounded-t-lg font-medium">
          Recipe 1
        </div>
        <div className="flex">
          <div
            className="flex flex-col gap-3 p-5"
            style={{ flex: 3, color: "white" }}
          >
            <div className="whitespace-pre-wrap" style={{ color: "#ededed" }}>
              {strings.map((s, index) => (
                <div key={`recepi-1-${index}`}>
                  <MarkdownViewer>{s}</MarkdownViewer>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const Data2 = () => {
  const { data } = useData();
  const { recipe_2 = "" } = data;
  if (!recipe_2) return <></>;
  const strings = recipe_2.split("\n");
  return (
    <div className="flex flex-col gap-2">
      <div
        className="flex flex-col rounded-lg"
        style={{ background: "#1f1f1f" }}
      >
        <div className="text-white p-4 bg-[#292929] rounded-t-lg font-medium">
          Recipe 2
        </div>
        <div className="flex">
          <div
            className="flex flex-col gap-3 p-5"
            style={{ flex: 3, color: "white" }}
          >
            <div className="whitespace-pre-wrap" style={{ color: "#ededed" }}>
              {strings.map((s, index) => (
                <div key={`recepi-2-${index}`}>
                  <MarkdownViewer>{s}</MarkdownViewer>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const WaferInfo = ({ title, image, deviations, errors }) => (
  <div className="flex-1 bg-[#1E1E1E] rounded-lg p-4">
    <h2 className="mb-4 text-xl font-semibold text-white">{title}</h2>
    <div className="flex items-center justify-center">
      <img
        src={image}
        alt={title}
        className=" mb-4 rounded-lg h-[200px] w-auto"
      />
    </div>
    <div className="text-white">
      <h3 className="mb-2 font-semibold">Deviations:</h3>
      <ul className="pl-5 mb-2 list-disc">
        {deviations.map((deviation, index) => (
          <li key={index} dangerouslySetInnerHTML={{ __html: deviation }} />
        ))}
      </ul>
      <h3 className="mb-2 font-semibold">Errors:</h3>
      <ul className="pl-5 list-disc">
        {errors.map((error, index) => (
          <li key={index} dangerouslySetInnerHTML={{ __html: error }} />
        ))}
      </ul>
    </div>
  </div>
);

export const WaferComparison = () => {
  return (
    <div className="flex gap-4">
      <WaferInfo
        title="Current Wafer"
        image="/images/current-wafer.png"
        deviations={[
          'Sidewall Angle: <span class="text-red-500">Off from the vertical</span>',
        ]}
        errors={[
          'Pattern Shift: <span class="text-red-500">1 nm lateral shift.</span>',
          'Surface Roughness: <span class="text-red-500">Increased roughness.</span>',
        ]}
      />
      <WaferInfo
        title="Expected"
        image="/images/expected-wafer.png"
        deviations={[
          'Sidewall Angle: <span class="text-green-500">Off from the vertical.</span>',
        ]}
        errors={[
          'Pattern Shift: <span class="text-green-500">pattern placement is accurate.</span>',
          'Surface Roughness: <span class="text-green-500">Smooth trench walls</span>',
        ]}
      />
    </div>
  );
};

export const Images = () => {
  return (
    <div className="">
      <div className="flex flex-col border border-[#2E2E2E] rounded-lg ">
        <div className="px-5 py-2.5 text-[#CBCBCB] border-b border-[#2E2E2E]">
          PlasmaPro 100 Cobra ICP RIE Etch
        </div>
        <div className="flex gap-10 p-8">
          <div className="flex items-end justify-center flex-1">
            <img src="/images/image-17.png" className="h-[200px]" />
          </div>
          <div className="flex items-center justify-center flex-1">
            <img
              src="/images/screenshot-20240808-at-1000121.png"
              className="h-[200px]"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

const MachineInfo = () => (
  <div className="flex flex-col bg-[#1E1E1E] rounded-lg p-4">
    <div className="p-5 text-[#CBCBCB]">
      Using<strong> ORBIS CMP System, Logitech LTD</strong> to etch:
    </div>
    <div className="flex justify-center">
      <img src="/images/logitech-machine.png" />
    </div>
  </div>
);

export const LeftPane = () => {
  const [message, setMessage] = useState(
    "I am trying to etch 2 μm of PECVD SiO2 using a ~4 μm PR mask to create a pattern of 20 * 60 μm. Recommend me 2 recipes."
  );
  const { isLoading, sendMessage, data } = useData();

  return (
    <div className="flex flex-col flex-1 overflow-y-scroll">
      <div className="flex flex-col gap-8 p-8">
        <WaferComparison />
        {/* <Images /> */}
        <MachineInfo />
      </div>
    </div>
  );
};
