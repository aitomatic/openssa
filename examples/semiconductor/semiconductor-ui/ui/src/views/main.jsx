import { LeftPane } from "./LeftPane";
import { RightPane } from "./RightPane";
import { Header } from "./Header";

export const MainView = () => {
  return (
    <div className="flex flex-col w-screen min-h-screen bg-black">
      <Header />
      <div className="flex">
        <LeftPane />
        <RightPane />
      </div>
    </div>
  );
};
