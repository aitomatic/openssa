import { useEffect, useRef, useState } from "react";
import { BACKEND_URL, useMessageStore } from "../store";
import { MarkdownViewer } from "../components/MarkdownViewer";
import axios from "axios";

const UserMessage = ({ avatar, user, content, type }) => {
  const strings = content.split("\n");
  return (
    <div className="flex items-start mb-4 space-x-3">
      <img
        src={type === "user" ? avatar : "/images/bot-avatar.svg"}
        alt="User avatar"
        className="w-8 h-8 rounded-full"
      />
      <div className="flex-1">
        <div className="mb-1 font-semibold text-white">{user}</div>
        <div className="p-3 text-white bg-[#1F1F1F] rounded-lg">
          <div className="whitespace-pre-wrap" style={{ color: "#ededed" }}>
            {strings.map((s, index) => (
              <div key={`Advice-2-${index}`}>
                <MarkdownViewer>{s}</MarkdownViewer>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export const ChatPane = () => {
  const { messages, addMessage } = useMessageStore();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      const userMessage = {
        user: "Zooey",
        content: input,
        avatar: "/images/user-avatar.png",
        type: "user",
      };
      addMessage(userMessage);
      setInput("");
      setIsLoading(true);

      try {
        // Simulating API call for bot response
        // const response = await axios.post(BACKEND_URL + "/data", {
        //   question: input,
        // });

        // const {
        //   recipe_1 = "",
        //   recipe_2 = "",
        //   agent_advice = "",
        // } = response.data;
        // const message = `Below is a comprehensive analysis that combines the information from multiple approaches: \n ${recipe_1}\ ${recipe_2}\n${agent_advice}`;

        // simulate 20s delay
        await new Promise((resolve) => setTimeout(resolve, 20_000));

        // Sample response message
        const message = "This is a test message";

        const botMessage = {
          user: "Etch Advisor",
          content: message,
          avatar: "/images/bot-avatar.png",
          type: "bot",
        };
        addMessage(botMessage);
      } catch (error) {
        console.error("Error getting bot response:", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex flex-col flex-1 h-full bg-black border-l border-[#2E2E2E]">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map(({ avatar, user, content, type }, index) => (
          <UserMessage
            key={index}
            avatar={avatar}
            user={user}
            content={content}
            type={type}
          />
        ))}
        {isLoading && <div className="text-white">Bot is typing...</div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="p-4">
        <div className="flex items-center p-4 text-sm bg-gray-800 rounded-lg">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Send your question..."
            className="flex-1 p-3 text-white bg-transparent focus:outline-none"
          />
          <svg
            width="44"
            height="44"
            viewBox="0 0 44 44"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="cursor-pointer"
          >
            <g filter="url(#filter0_d_16265_49811)">
              <rect x="2" y="1" width="40" height="40" rx="8" fill="#003D87" />
              <rect
                x="2.5"
                y="1.5"
                width="39"
                height="39"
                rx="7.5"
                stroke="#043A7B"
              />
              <g clip-path="url(#clip0_16265_49811)">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M31.9909 11.0059L24.9653 31.0048L20.2051 23.9698L25.0856 19.0893L23.9071 17.9108L19.0271 22.7908L11.9922 18.0241L31.9909 11.0059Z"
                  fill="#43A1FC"
                />
              </g>
            </g>
            <defs>
              <filter
                id="filter0_d_16265_49811"
                x="0"
                y="0"
                width="44"
                height="44"
                filterUnits="userSpaceOnUse"
                color-interpolation-filters="sRGB"
              >
                <feFlood flood-opacity="0" result="BackgroundImageFix" />
                <feColorMatrix
                  in="SourceAlpha"
                  type="matrix"
                  values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                  result="hardAlpha"
                />
                <feOffset dy="1" />
                <feGaussianBlur stdDeviation="1" />
                <feColorMatrix
                  type="matrix"
                  values="0 0 0 0 0.0627451 0 0 0 0 0.0941176 0 0 0 0 0.156863 0 0 0 0.05 0"
                />
                <feBlend
                  mode="normal"
                  in2="BackgroundImageFix"
                  result="effect1_dropShadow_16265_49811"
                />
                <feBlend
                  mode="normal"
                  in="SourceGraphic"
                  in2="effect1_dropShadow_16265_49811"
                  result="shape"
                />
              </filter>
              <clipPath id="clip0_16265_49811">
                <rect
                  width="20"
                  height="20"
                  fill="white"
                  transform="translate(12 11)"
                />
              </clipPath>
            </defs>
          </svg>
        </div>
      </form>
    </div>
  );
};
