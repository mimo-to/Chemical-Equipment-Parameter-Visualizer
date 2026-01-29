import { useState } from 'react';
import Upload from './Upload';
import Charts from './Charts';
import History from './History';
import ErrorBoundary from './ErrorBoundary';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
    const [datasetId, setDatasetId] = useState(null);
    const [activeTab, setActiveTab] = useState('upload');
    const { logout } = useAuth();

    const handleUploadSuccess = (id) => {
        setDatasetId(id);
        setActiveTab('charts'); // Auto-switch to charts
    };

    return (
        <ErrorBoundary>
            <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h1>Dashboard</h1>
                    <button onClick={logout} style={{ padding: '8px 16px', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                        Logout
                    </button>
                </div>

                <div style={{ marginBottom: '20px', borderBottom: '1px solid #ccc' }}>
                    <button
                        onClick={() => setActiveTab('upload')}
                        style={{ padding: '10px 20px', marginRight: '5px', background: activeTab === 'upload' ? '#007bff' : 'transparent', color: activeTab === 'upload' ? 'white' : '#e0e0e0', border: 'none', borderRadius: '4px 4px 0 0', cursor: 'pointer', fontWeight: 'bold' }}
                    >
                        Upload
                    </button>
                    <button
                        onClick={() => setActiveTab('charts')}
                        style={{ padding: '10px 20px', marginRight: '5px', background: activeTab === 'charts' ? '#007bff' : 'transparent', color: activeTab === 'charts' ? 'white' : (datasetId ? '#e0e0e0' : '#666'), border: 'none', borderRadius: '4px 4px 0 0', cursor: datasetId ? 'pointer' : 'not-allowed', fontWeight: 'bold' }}
                        disabled={!datasetId}
                    >
                        Charts
                    </button>
                    <button
                        onClick={() => setActiveTab('history')}
                        style={{ padding: '10px 20px', background: activeTab === 'history' ? '#007bff' : 'transparent', color: activeTab === 'history' ? 'white' : '#e0e0e0', border: 'none', borderRadius: '4px 4px 0 0', cursor: 'pointer', fontWeight: 'bold' }}
                    >
                        History
                    </button>
                </div>

                <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '0 4px 4px 4px', background: '#f9f9f9', color: '#333' }}>
                    {activeTab === 'upload' && <Upload onUploadSuccess={handleUploadSuccess} />}
                    {activeTab === 'charts' && <Charts datasetId={datasetId} />}
                    {activeTab === 'history' && <History refreshTrigger={datasetId} />}
                </div>
            </div>
        </ErrorBoundary>
    );
};

export default Dashboard;
