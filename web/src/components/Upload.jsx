import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { uploadCSV } from '../services/api';

const Upload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');
    const { token, logout } = useAuth();

    const MAX_SIZE = 10 * 1024 * 1024;

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError('');
        setStats(null);
    };

    const handleUpload = async () => {
        if (!file) return;

        setError('');
        setStats(null);

        if (!file.name.toLowerCase().endsWith('.csv')) {
            setError('Invalid file type. Only .csv files are allowed.');
            return;
        }

        if (file.size > MAX_SIZE) {
            setError(`File too large. Max size is ${MAX_SIZE / (1024 * 1024)}MB.`);
            return;
        }

        setLoading(true);
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
            const input = document.getElementById('fileInput');
            if (input) input.value = '';
        }
    };

    return (
        <div className="upload-section">
            <h3>Data Acquisition</h3>
            <div className="file-input-row">
                <input
                    id="fileInput"
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                />
                <button
                    onClick={handleUpload}
                    disabled={!file || loading}
                    className="btn-primary"
                >
                    {loading ? 'Processing...' : 'Analyze'}
                </button>
            </div>

            {error && <div className="alert alert-error">Error: {error}</div>}

            {stats && (
                <div className="alert alert-success">
                    <div className="stats-display">
                        <h4>Analysis Complete</h4>
                        <div className="stat-row">
                            <span className="stat-label">Total Records</span>
                            <span className="stat-value">{stats.total_count}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Flowrate</span>
                            <span className="stat-value">{Number(stats.avg_flowrate).toFixed(2)}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Pressure</span>
                            <span className="stat-value">{Number(stats.avg_pressure).toFixed(2)}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Temperature</span>
                            <span className="stat-value">{Number(stats.avg_temperature).toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Upload;
