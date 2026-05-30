// src/plugins/axios.js
import axios from 'axios';

function normalizeApiBase(url) {
  const base = (url || 'http://localhost:5000').replace(/\/$/, '');
  return base.endsWith('/api') ? base : `${base}/api`;
}

const apiBase = normalizeApiBase(import.meta.env.VITE_API_BASE_URL);

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