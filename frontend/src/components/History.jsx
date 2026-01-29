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
            <h3>Upload History (Last 5)</h3>
            {history.length === 0 ? (
                <p>No history available.</p>
            ) : (
                <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                    <thead>
                        <tr>
                            <th style={{ padding: '8px' }}>Filename</th>
                            <th style={{ padding: '8px' }}>Uploaded At</th>
                            <th style={{ padding: '8px' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map((item) => (
                            <tr key={item.id}>
                                <td style={{ padding: '8px' }}>{item.filename}</td>
                                <td style={{ padding: '8px' }}>{new Date(item.uploaded_at).toLocaleString()}</td>
                                <td style={{ padding: '8px', textAlign: 'center' }}>
                                    <button onClick={() => handleDownload(item.id, item.filename)}>
                                        Download PDF
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default History;
