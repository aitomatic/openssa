export const RightPane = () => {
  return (
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
        <div className="text-white">Steps to Optimize the Etching Process</div>
        <div>
          <img className="w-full" src="/public/images/image-16.png" />
        </div>
      </div>
    </div>
  );
};
