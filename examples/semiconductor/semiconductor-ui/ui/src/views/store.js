import { create } from "zustand";
import axios from "axios";

export const useData = create((set) => ({
  data: {},
  getData: async () => {
    try {
      const response = await axios.get("http://localhost:9000/data");
      set({ data: response.data });
    } catch (error) {
      console.error(error);
    }
  },
}));
