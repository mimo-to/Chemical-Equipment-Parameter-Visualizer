import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getHistory, downloadReport } from '../services/api';

const History = ({ refreshTrigger }) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
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
            alert('Failed to download report');
        }
    };

    if (loading && history.length === 0) return <p>Loading history...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;

    return (
        <div style={{ marginTop: '30px' }}>
            <h3 style={{ borderBottom: '2px solid #007bff', paddingBottom: '10px', marginBottom: '15px' }}>Upload History (Last 5)</h3>
            {history.length === 0 ? (
                <p style={{ color: '#666', fontStyle: 'italic' }}>No history available yet.</p>
            ) : (
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                        <thead>
                            <tr style={{ background: '#f8f9fa', borderBottom: '2px solid #dee2e6' }}>
                                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>Filename</th>
                                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>Uploaded At</th>
                                <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600', color: '#495057' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item, index) => (
                                <tr key={item.id} style={{ borderBottom: '1px solid #dee2e6', background: index % 2 === 0 ? 'white' : '#f8f9fa' }}>
                                    <td style={{ padding: '12px', color: '#212529' }}>{item.filename}</td>
                                    <td style={{ padding: '12px', color: '#212529' }}>{new Date(item.uploaded_at).toLocaleString()}</td>
                                    <td style={{ padding: '12px', textAlign: 'center' }}>
                                        <button
                                            onClick={() => handleDownload(item.id, item.filename)}
                                            style={{
                                                padding: '6px 12px',
                                                background: '#17a2b8',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer',
                                                fontSize: '0.9rem'
                                            }}
                                        >
                                            Download PDF
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
