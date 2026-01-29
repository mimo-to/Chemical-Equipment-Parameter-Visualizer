import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { uploadCSV } from '../services/api';

const Upload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');
    const { token, logout } = useAuth();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError('');
        setStats(null);
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setError('');
        try {
            const data = await uploadCSV(file, token);
            setStats(data);
            if (onUploadSuccess && data.id) {
                onUploadSuccess(data.id);
            }
        } catch (err) {
            if (err.message === 'Unauthorized') {
                logout();
                return;
            }
            setError(err.message || 'Upload failed');
        } finally {
            setLoading(false);
            const fileInput = document.getElementById('fileInput');
            if (fileInput) fileInput.value = '';
        }
    };

    return (
        <div style={{ marginBottom: '20px' }}>
            <h3>Upload CSV</h3>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '15px' }}>
                <input id="fileInput" type="file" accept=".csv" onChange={handleFileChange} style={{ padding: '5px' }} />
                <button
                    onClick={handleUpload}
                    disabled={!file || loading}
                    style={{
                        padding: '8px 20px',
                        background: !file || loading ? '#ccc' : '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: !file || loading ? 'not-allowed' : 'pointer',
                        fontWeight: 'bold'
                    }}
                >
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </div>

            {error && <div style={{ padding: '10px', background: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '15px' }}>Error: {error}</div>}

            {stats && (
                <div style={{ padding: '15px', background: '#d4edda', color: '#155724', borderRadius: '4px', border: '1px solid #c3e6cb' }}>
                    <h4 style={{ margin: '0 0 10px 0' }}>Upload Summary</h4>
                    <p style={{ margin: '5px 0' }}><strong>Total Records:</strong> {stats.total_count}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Flowrate:</strong> {stats.averages.avg_flowrate?.toFixed(2)}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Pressure:</strong> {stats.averages.avg_pressure?.toFixed(2)}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Temperature:</strong> {stats.averages.avg_temperature?.toFixed(2)}</p>
                </div>
            )}
        </div>
    );
};

export default Upload;
