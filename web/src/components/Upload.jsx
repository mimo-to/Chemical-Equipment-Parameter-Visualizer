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

    const MAX_FILE_SIZE = 10 * 1024 * 1024;

    const handleUpload = async () => {
        if (!file) return;

        setError('');
        setStats(null);

        if (!file.name.toLowerCase().endsWith('.csv')) {
            const msg = 'Invalid file type. Only .csv files are allowed.';
            console.warn(`[Upload] Pre-validation failed: ${msg}`);
            setError(msg);
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            const msg = `File too large. Max size is ${MAX_FILE_SIZE / (1024 * 1024)}MB.`;
            console.warn(`[Upload] Pre-validation failed: ${msg}`);
            setError(msg);
            return;
        }

        console.log(`[Upload] Starting upload: ${file.name} (${file.size} bytes)`);
        setLoading(true);
        try {
            const data = await uploadCSV(file, token);
            console.log('[Upload] Success, Stats received');
            setStats(data);
            if (onUploadSuccess && data.id) {
                onUploadSuccess(data.id);
            }
        } catch (err) {
            console.error('[Upload] Failed:', err.message);
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
                    className="btn-primary"
                    style={{ padding: '0.6rem 1.2rem' }}
                >
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </div>

            {error && <div className="alert alert-error">Error: {error}</div>}

            {stats && (
                <div className="alert alert-success">
                    <h4 style={{ margin: '0 0 10px 0', color: 'inherit' }}>Upload Summary</h4>
                    <p style={{ margin: '5px 0' }}><strong>Total Records:</strong> {stats.total_count}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Flowrate:</strong> {Number(stats.avg_flowrate).toFixed(2)}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Pressure:</strong> {Number(stats.avg_pressure).toFixed(2)}</p>
                    <p style={{ margin: '5px 0' }}><strong>Avg Temperature:</strong> {Number(stats.avg_temperature).toFixed(2)}</p>
                </div>
            )}
        </div>
    );
};

export default Upload;
