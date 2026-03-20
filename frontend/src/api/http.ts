import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("class_pets_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
