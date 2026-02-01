const BASE_URL = 'http://127.0.0.1:8000/api';

const api = async (endpoint, options = {}) => {
  const headers = { ...options.headers };
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (options.responseType === 'blob') {
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || 'Request failed');
    }
    return response.blob();
  }

  const data = await response.json();
  if (!response.ok) {
    if (response.status === 401) throw new Error('Unauthorized');
    throw new Error(data.error || 'Request failed');
  }
  return data;
};

export const loginUser = (username, password) =>
  api('/login/', { method: 'POST', body: JSON.stringify({ username, password }) });

export const uploadCSV = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);
  return api('/upload/', {
    method: 'POST',
    headers: { 'Authorization': `Token ${token}` },
    body: formData
  });
};

export const getVisualization = (id, token) =>
  api(`/dataset/${id}/visualization/`, { headers: { 'Authorization': `Token ${token}` } });

export const getHistory = (token) =>
  api('/history/', { headers: { 'Authorization': `Token ${token}` } });

export const downloadReport = (id, token) =>
  api(`/report/${id}/`, { headers: { 'Authorization': `Token ${token}` }, responseType: 'blob' });

export const compareDatasets = (id1, id2, token) =>
  api('/compare/', {
    method: 'POST',
    headers: { 'Authorization': `Token ${token}` },
    body: JSON.stringify({ dataset1: id1, dataset2: id2 })
  });
