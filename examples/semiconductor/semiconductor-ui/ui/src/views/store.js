import { create } from "zustand";
import axios from "axios";

const BACKEND_URL = "http://localhost:9000";

export const SAMPLE_DATA = {
  recipe_1:
    "Gases & Flow Rates:\n        CHF3: 40 sccm\n        Ar: 10 sccm\n        O2: 3 sccm\n    ICP Power:\n        800 W\n    RF Power: \n        30 W\n    Pressure: \n        10 mTorr\n    Etch Time: \n        Approximately 10 minutes (adjust based on actual etch rate and periodic depth measurements)\n    Pros: \n        High Etch Rate: The higher ICP power and CHF3 flow rate will result in a faster etch rate, reducing overall process time.\n        Good Anisotropy: The combination of CHF3 and O2 helps in achieving good anisotropic profiles, which is crucial for pattern fidelity.\n    Cons:\n        Potential for Physical Damage: Higher ICP power can lead to more physical damage to the PR mask and underlying layers.\n        Less Control Over Uniformity: Faster etch rates can sometimes lead to less uniform etching across the wafer.",
  recipe_2:
    "Gases & Flow Rates:\n        CHF3: 30 sccm\n        Ar: 5 sccm\n        O2: 2 sccm\n    ICP Power:\n        600 W\n    RF Power:\n        20 W\n    Pressure:\n        15 mTorr\n    Etch Time:\n        Approximately 15 minutes (adjust based on actual etch rate and periodic depth measurements)\n    Pros:\n        High Anisotropy: Lower RF power and optimized gas flow rates help in achieving highly anisotropic etch profiles, which is beneficial for maintaining pattern dimensions.\n        Reduced Physical Damage: Lower ICP power reduces the risk of physical damage to the PR mask and underlying layers.\n    Cons:\n        Slower Etch Rate: The etch rate will be slower compared to the high etch rate recipe, increasing the overall process time.\n        Potential for Polymer Build-Up: Lower O2 flow rates might lead to polymer build-up, which could affect etch uniformity and profile.",
  agent_advice:
    "Etch Rate and Uniformity: Regularly measure the etch depth to ensure uniformity and to adjust the etch time as needed. The etch rate can vary across the wafer and over time.\n    End-Point Detection: Utilize optical emission spectroscopy (OES) or interferometry if available on your system to accurately determine when the desired etch depth is reached.\n    Safety Procedures: Always follow safety protocols when handling gases and operating the ICP-RIE system. Confirm with your facility and equipment manager that the chosen recipes are compatible with your system to avoid any damage or contamination.\n```",
};

export const useData = create((set) => ({
  data: {},
  isLoading: false,
  getData: async () => {
    try {
      const response = await axios.get(BACKEND_URL + "/data");
      set({ data: response.data });
    } catch (error) {
      console.error(error);
    }
  },
  sendMessage: async (message) => {
    try {
      set({ isLoading: true });
      const res = await axios.post(BACKEND_URL + "/data", {
        question: message,
      });
      set({ data: res.data, isLoading: false });
    } catch (error) {
      console.error(error);
    }
  },
}));
