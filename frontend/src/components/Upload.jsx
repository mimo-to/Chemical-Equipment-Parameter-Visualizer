import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { uploadCSV } from '../services/api';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');
    const { token } = useAuth();

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
        } catch (err) {
            setError(err.message || 'Upload failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc' }}>
            <h2>Upload CSV</h2>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!file || loading}>
                {loading ? 'Uploading...' : 'Upload'}
            </button>

            {error && <p style={{ color: 'red' }}>Error: {error}</p>}

            {stats && (
                <div style={{ marginTop: '10px' }}>
                    <h3>Upload Summary</h3>
                    <p>Total Records: {stats.total_count}</p>
                    <p>Avg Flowrate: {stats.avg_flowrate?.toFixed(2)}</p>
                    <p>Avg Pressure: {stats.avg_pressure?.toFixed(2)}</p>
                    <p>Avg Temperature: {stats.avg_temperature?.toFixed(2)}</p>
                </div>
            )}
        </div>
    );
};

export default Upload;
