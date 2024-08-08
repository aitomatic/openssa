import { create } from "zustand";
import axios from "axios";

const BACKEND_URL = "http://localhost:9000";

export const SAMPLE_DATA = {
  recipe_1: `Gases & Flow Rates:

          CHF3: 40 sccm
          Ar: 10 sccm
          O2: 3 sccm
      ICP Power:
          800 W
      RF Power: 
          30 W
      Pressure: 
          10 mTorr
      Etch Time: 
          Approximately 10 minutes (adjust based on actual etch rate and periodic depth measurements)
      Pros: 
          High Etch Rate: The higher ICP power and CHF3 flow rate will result in a faster etch rate, reducing overall process time.
          Good Anisotropy: The combination of CHF3 and O2 helps in achieving good anisotropic profiles, which is crucial for pattern fidelity.
      Cons:
          Potential for Physical Damage: Higher ICP power can lead to more physical damage to the PR mask and underlying layers.
          Less Control Over Uniformity: Faster etch rates can sometimes lead to less uniform etching across the wafer.`,
  recipe_2: `
Gases & Flow Rates:
  CHF3: 30 sccm
  
  Ar: 5 sccm
            O2: 2 sccm
        ICP Power:
            600 W
        RF Power:
            20 W
        Pressure:
            15 mTorr
        Etch Time:
            Approximately 15 minutes (adjust based on actual etch rate and periodic depth measurements)
        Pros:
            High Anisotropy: Lower RF power and optimized gas flow rates help in achieving highly anisotropic etch profiles, which is beneficial for maintaining pattern dimensions.
            Reduced Physical Damage: Lower ICP power reduces the risk of physical damage to the PR mask and underlying layers.
        Cons:
            Slower Etch Rate: The etch rate will be slower compared to the high etch rate recipe, increasing the overall process time.
            Potential for Polymer Build-Up: Lower O2 flow rates might lead to polymer build-up, which could affect etch uniformity and profile.`,
  agent_advice: `#### Etch Rate and Uniformity: 
  Regularly measure the etch depth to ensure uniformity and to adjust the etch time as needed. The etch rate can vary across the wafer and over time.


  End-Point Detection: Utilize optical emission spectroscopy (OES) or interferometry if available on your system to accurately determine when the desired etch depth is reached.
        Safety Procedures: Always follow safety protocols when handling gases and operating the ICP-RIE system. Confirm with your facility and equipment manager that the chosen recipes are compatible with your system to avoid any damage or contamination.
    `,
};

export const sample_q =
  "How to etch 2 um silicon dioxide (PR mask) using ICP RIE Plasmalab System 100? Any suggestions for recipe? I am trying to etch 2 μm of PECVD SiO2 using a ~4 μm PR mask to create a pattern of 20 * 60 μm. I am using the Oxford ICP-RIE Plasmalab System 100. Recommend me 2 recipes and their pros/cons.";

export const useData = create((set) => ({
  data: {},
  // data: SAMPLE_DATA,
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
