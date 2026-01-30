const BASE_URL = 'http://127.0.0.1:8000/api';

export const apiRequest = async (endpoint, options = {}) => {
    const url = `${BASE_URL}${endpoint}`;
    const headers = { ...options.headers };

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }

    try {
        console.log(`[API] Request: ${options.method || 'GET'} ${url}`);
        const response = await fetch(url, {
            ...options,
            headers: headers,
        });

        if (options.responseType === 'blob') {
            if (!response.ok) {
                const errorData = await response.json();
                console.error(`[API] Error ${response.status}:`, errorData.error || 'Unknown error');
                throw new Error(errorData.error || 'Something went wrong');
            }
            console.log(`[API] Success ${response.status}:`, url);
            return response.blob();
        }

        const data = await response.json();

        if (!response.ok) {
            console.error(`[API] Error ${response.status}:`, data.error || 'Unknown error');
            throw new Error(data.error || 'Something went wrong');
        }

        console.log(`[API] Success ${response.status}:`, url);
        return data;
    } catch (error) {
        console.error('[API] Request Failed:', error.message);
        throw error;
    }
};

export const loginUser = async (username, password) => {
    return apiRequest('/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
};

export const uploadCSV = async (file, token) => {
    const formData = new FormData();
    formData.append('file', file);
    
    console.log(`[API] Request: POST ${BASE_URL}/upload/`);
    const response = await fetch(`${BASE_URL}/upload/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`
        },
        body: formData
    });

    const data = await response.json();

    if (!response.ok) {
        if (response.status === 401) {
            throw new Error('Unauthorized');
        }
        throw new Error(data.error || 'Upload failed');
    }

    return data;
};

export const getVisualization = async (id, token) => {
    const response = await fetch(`${BASE_URL}/dataset/${id}/visualization/`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error('Failed to fetch visualization data');
    }

    return await response.json();
};

export const getHistory = async (token) => {
    const response = await fetch(`${BASE_URL}/history/`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error('Failed to fetch history');
    }

    return await response.json();
};

export const downloadReport = async (id, token) => {
    const response = await fetch(`${BASE_URL}/report/${id}/`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error('Failed to download report');
    }

    return await response.blob();
};
