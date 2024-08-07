import { useState } from "react";
import { useData } from "../store";

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
  return (
    <div className="flex flex-col gap-2">
      <div className="text-white">Recipe 1</div>
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
              {recipe_1}
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
  return (
    <div className="flex flex-col gap-2">
      <div className="text-white">Recipe 2</div>
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
              {recipe_2}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const AgentAdvice = () => {
  const { data } = useData();
  const { agent_advice = "" } = data;
  if (!agent_advice) return <></>;
  return (
    <div className="flex flex-col gap-2">
      <div className="text-white">Agent Advice </div>
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
              {agent_advice}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const LeftPane = () => {
  const [message, setMessage] = useState("");
  const { isLoading, sendMessage } = useData();

  return (
    <div className="flex flex-col flex-1 gap-8 p-8">
      <div className="flex flex-col gap-2">
        <div className="text-white">Question</div>
        <div
          className="flex flex-col border rounded-lg"
          style={{ borderColor: "#454545", backgroundColor: "#1a1a1a" }}
        >
          <div className="p-5">
            <textarea
              rows={4}
              className="w-full resize-none"
              value={message}
              onChange={(e) => setMessage(e.currentTarget.value)}
            ></textarea>
          </div>
          <div className="flex justify-end p-5">
            <button
              className="px-5 py-2 text-black bg-white rounded-lg"
              onClick={() => sendMessage(message)}
              disabled={isLoading}
            >
              Solve
            </button>
          </div>
        </div>
      </div>
      {/* <Specification />
      <Plan /> */}
      {isLoading && <div className="text-white">Requesting data...</div>}
      <Data1 />
      <Data2 />
    </div>
  );
};
