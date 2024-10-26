import { LeftPane } from "./LeftPane";
import { RightPane } from "./RightPane";
import { TitleHeader } from "./Header";

export const MainView = () => {
  return (
    <div className="flex flex-col w-screen min-h-screen bg-black">
      <TitleHeader />
      <div className="flex">
        <LeftPane />
        <RightPane />
      </div>
    </div>
  );
};
