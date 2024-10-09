const { useState } = React;

const store = zustandVanilla((set) => ({
  count: 0,
  inc: () => set((state) => ({ count: state.count + 1 })),
}));

function MyApp() {
  const { count, inc } = useZustand.useZustand(store, (state) => state);
  const [str, setStr] = useState("Hello, Tailwind CSS!");

  return (
    <div className="flex w-screen h-screen justify-center items-center flex flex-col">
      <div className="flex px-2 py-2 border-b border-gray-200 w-screen justify-center">
        <div class="w-full">
          <div class="w-full margin-auto">
            <ol class="flex justify-center w-full text-xs text-gray-900 font-medium sm:text-base w-full">
              <li class="flex items-center w-full relative text-indigo-600  after:content-['']  after:w-full after:h-0.5  after:bg-indigo-600 after:inline-block after:absolute lg:after:top-5 after:top-3 after:left-4">
                <div class="block whitespace-nowrap z-10">
                  <span class="w-6 h-6 bg-indigo-600 border-2 border-transparent rounded-full flex justify-center items-center mx-auto mb-3 text-sm text-white lg:w-10 lg:h-10">
                    1
                  </span>
                  Step 1
                </div>
              </li>
              <li class="flex w-full relative text-gray-900  after:content-['']  after:w-full after:h-0.5  after:bg-gray-200 after:inline-block after:absolute lg:after:top-5 after:top-3 after:left-4">
                <div class="block whitespace-nowrap z-10">
                  <span class="w-6 h-6 bg-indigo-50 border-2 border-indigo-600 rounded-full flex justify-center items-center mx-auto mb-3 text-sm text-indigo-600 lg:w-10 lg:h-10">
                    2
                  </span>
                  Step 2
                </div>
              </li>
              <li class="flex w-full relative text-gray-900  after:content-['']  after:w-full after:h-0.5  after:bg-gray-200 after:inline-block after:absolute lg:after:top-5  after:top-3 after:left-4">
                <div class="block whitespace-nowrap z-10">
                  <span class="w-6 h-6 bg-gray-50 border-2 border-gray-200 rounded-full flex justify-center items-center mx-auto mb-3 text-sm  lg:w-10 lg:h-10">
                    3
                  </span>
                  Step 3
                </div>
              </li>
            </ol>
          </div>
        </div>
      </div>
      <div className="flex flex-1 h-screen flex-col p-8 justify-start">
        <div className="flex flex-col gap-2">
          <div className="text-gray-900 font-medium">Question</div>
          <div className=" bg-white rounded-lg shadow-md p-8">
            <input
              className="border-none"
              value={str}
              onChange={(e) => setStr(e.currentTarget.value)}
            />
          </div>
        </div>
      </div>
      <div className=" bg-white rounded-lg shadow-md p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Hello, Tailwind CSS!
        </h1>
        <p className="text-gray-700">
          This is a simple HTML file with Tailwind CSS included. {count}
        </p>
        <button
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={inc}
        >
          Click Me
        </button>
      </div>
    </div>
  );
}

const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(<MyApp />);
