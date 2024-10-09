import { LeftPane } from "./LeftPane";
// import { RightPane } from "./RightPane";
import { TitleHeader } from "./Header";
import { ChatPane } from "./ChatPane";

export const MainView = () => {
  return (
    <div className="flex flex-col w-screen h-screen overflow-y-scroll bg-black">
      <TitleHeader />
      <div className="flex flex-col flex-1 overflow-y-scroll">
        <div className="flex overflow-y-scroll">
          <LeftPane />
          {/* <RightPane /> */}
          <ChatPane />
        </div>
      </div>
    </div>
  );
};
