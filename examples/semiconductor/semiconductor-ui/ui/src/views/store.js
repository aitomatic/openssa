import { create } from "zustand";
import axios from "axios";

const BACKEND_URL = "http://localhost:9000";

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
      const res = await axios.post(BACKEND_URL + "/data", { message });
      set({ data: res.data, isLoading: false });
    } catch (error) {
      console.error(error);
    }
  },
}));
