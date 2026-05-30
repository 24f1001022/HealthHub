// src/plugins/axios.js
import axios from 'axios';

function normalizeApiBase(url) {
  const base = (url || 'http://localhost:5000').replace(/\/$/, '');
  return base.endsWith('/api') ? base : `${base}/api`;
}

function resolveApiBase() {
  if (import.meta.env.DEV) {
    return normalizeApiBase(import.meta.env.VITE_API_BASE_URL);
  }
  // Production on Vercel: same-origin /api proxy (vercel.json) — fixes login cookies
  if (import.meta.env.VITE_USE_VERCEL_PROXY === 'false' && import.meta.env.VITE_API_BASE_URL) {
    return normalizeApiBase(import.meta.env.VITE_API_BASE_URL);
  }
  return '/api';
}

const apiBase = resolveApiBase();
const useVercelProxy = apiBase === '/api';

/** Origin for export/static URLs */
export const apiOrigin = useVercelProxy
  ? ''
  : apiBase.replace(/\/api\/?$/, '');

const axiosInstance = axios.create({
  baseURL: apiBase,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default axiosInstance;
