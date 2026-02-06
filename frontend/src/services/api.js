import axios from 'axios';

// In dev mode (Vite dev server), call the backend directly.
// In production (served from FastAPI), use relative URLs (same origin).
const API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000' : '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minute timeout for LLM calls
});

/**
 * Upload log messages for processing
 * @param {string[]} logs - Array of log strings
 */
export const uploadLogs = async (logs) => {
  const response = await api.post('/upload_logs', { logs });
  return response.data;
};

/**
 * Upload a file containing logs
 * @param {File} file - File object (JSON, CSV, or text)
 */
export const uploadLogFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload_logs', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

/**
 * Load pre-built demo logs
 */
export const uploadDemoLogs = async () => {
  const response = await api.post('/upload_demo_logs');
  return response.data;
};

/**
 * Analyze an incident
 * @param {string[]|null} logs - Optional specific logs to analyze
 * @param {string|null} query - Optional incident description
 */
export const analyzeIncident = async (logs = null, query = null) => {
  const body = {};
  if (logs) body.logs = logs;
  if (query) body.query = query;
  const response = await api.post('/analyze_incident', body);
  return response.data;
};

/**
 * Get all stored analysis results
 */
export const getResults = async () => {
  const response = await api.get('/results');
  return response.data;
};

export default api;
