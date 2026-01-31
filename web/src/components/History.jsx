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

    useEffect(() => {
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

        fetchHistory();
    }, [token, refreshTrigger]);

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

    if (loading && history.length === 0) {
        return <p className="loading-state">Loading experiment log...</p>;
    }

    if (error) {
        return <p className="alert alert-error">{error}</p>;
    }

    return (
        <div className="history-section">
            <h3>Experiment Log (Last 5)</h3>

            {downloadError && <div className="download-error">{downloadError}</div>}

            {history.length === 0 ? (
                <p className="empty-state">No experiments recorded yet.</p>
            ) : (
                <div className="table-container">
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
