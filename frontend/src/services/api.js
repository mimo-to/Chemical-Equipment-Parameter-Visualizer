const BASE_URL = 'http://127.0.0.1:8000/api';

export const loginUser = async (username, password) => {
    const response = await fetch(`${BASE_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) {
        throw new Error('Login failed');
    }
    
    return await response.json();
};

export const uploadCSV = async (file, token) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${BASE_URL}/upload/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`
        },
        body: formData
    });

    if (!response.ok) {
        throw new Error('Upload failed');
    }

    return await response.json();
};
