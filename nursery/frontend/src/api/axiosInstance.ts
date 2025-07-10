// src/api/axiosInstance.ts
import axios from "axios";

// see .env file for environment variables
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  // you can add other defaults here, like headers
});

export default axiosInstance;
