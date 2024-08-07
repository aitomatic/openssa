import { useEffect } from "react";
import { useData } from "./store";
import { LeftPane } from "./LeftPane";
import { RightPane } from "./RightPane";
import { Header } from "./Header";

export const MainView = () => {
  const { data, getData } = useData();
  console.log(data);

  useEffect(() => {
    getData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
