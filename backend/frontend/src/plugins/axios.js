// src/plugins/axios.js
import axios from 'axios';

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

/** Origin without /api — for static export file downloads */
export const apiOrigin = apiBase.replace(/\/api\/?$/, '');

const axiosInstance = axios.create({
  baseURL: apiBase,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default axiosInstance;