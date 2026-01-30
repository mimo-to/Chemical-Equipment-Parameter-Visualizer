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

    if (loading && history.length === 0) return <p>Loading history...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;

    return (
        <div style={{ marginTop: '30px' }}>
            <h3 style={{ borderBottom: '2px solid #007bff', paddingBottom: '10px', marginBottom: '15px' }}>Upload History (Last 5)</h3>

            {downloadError && (
                <div style={{ background: '#f8d7da', color: '#721c24', padding: '10px', marginBottom: '10px', borderRadius: '4px' }}>
                    {downloadError}
                </div>
            )}

            {history.length === 0 ? (
                <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>No history available yet.</p>
            ) : (
                <div className="table-container">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Filename</th>
                                <th>Uploaded At</th>
                                <th style={{ textAlign: 'center' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.filename}</td>
                                    <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                                    <td style={{ textAlign: 'center' }}>
                                        <button
                                            onClick={() => handleDownload(item.id, item.filename)}
                                            disabled={downloadingId === item.id}
                                            className="btn-primary"
                                            style={{ padding: '0.4rem 0.8rem', fontSize: '0.875rem' }}
                                        >
                                            {downloadingId === item.id ? 'Downloading...' : 'Download PDF'}
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
