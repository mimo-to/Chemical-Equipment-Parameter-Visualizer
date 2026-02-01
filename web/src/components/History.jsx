import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getHistory, downloadReport } from '../services/api';

const History = ({ refreshTrigger }) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [downloadingId, setDownloadingId] = useState(null);
    const [error, setError] = useState('');
    const [downloadError, setDownloadError] = useState('');
    const { token } = useAuth();

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const data = await getHistory(token);
            setHistory(data);
            setError('');
        } catch (err) {
            setError('Failed to load history');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, [token, refreshTrigger]);

    const handleRefresh = () => {
        fetchHistory();
    };

    const handleDownload = async (id, filename) => {
        setDownloadingId(id);
        setDownloadError('');
        try {
            const blob = await downloadReport(id, token);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `report_${id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            setDownloadError(`Failed to download report for ${filename}`);
            setTimeout(() => setDownloadError(''), 5000);
        } finally {
            setDownloadingId(null);
        }
    };

    if (error) {
        return <p className="alert alert-error">{error}</p>;
    }

    const getStorageIndicator = () => {
        const filled = history.length;
        const empty = 5 - filled;
        return '⬢'.repeat(filled) + '⬡'.repeat(empty);
    };

    return (
        <div className="history-section">
            <div className="history-header">
                <h3>Experiment Log</h3>
                <span className="storage-indicator">
                    {getStorageIndicator()} {history.length}/5
                </span>
                <button
                    onClick={handleRefresh}
                    className="btn-refresh"
                    disabled={loading}
                >
                    {loading ? 'LOADING...' : 'REFRESH'}
                </button>
            </div>

            {downloadError && <div className="download-error">{downloadError}</div>}

            {history.length === 0 && !loading ? (
                <p className="empty-state">No experiments recorded yet.</p>
            ) : history.length === 0 && loading ? (
                <p className="loading-state">Loading experiment log...</p>
            ) : (
                <div className={`table-container ${loading ? 'is-loading' : ''}`}>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Filename</th>
                                <th>Timestamp</th>
                                <th className="actions">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.filename}</td>
                                    <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                                    <td className="actions">
                                        <button
                                            onClick={() => handleDownload(item.id, item.filename)}
                                            disabled={downloadingId === item.id}
                                            className="btn-primary"
                                        >
                                            {downloadingId === item.id ? 'Exporting...' : 'Export PDF'}
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default History;
