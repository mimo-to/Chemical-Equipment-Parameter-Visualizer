import { useState } from 'react';
import Upload from './Upload';
import Charts from './Charts';
import History from './History';
import Compare from './Compare';
import ErrorBoundary from './ErrorBoundary';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
    const [datasetId, setDatasetId] = useState(null);
    const [activeTab, setActiveTab] = useState('upload');
    const { logout } = useAuth();

    const handleUploadSuccess = (id) => {
        setDatasetId(id);
        setActiveTab('charts');
    };

    return (
        <ErrorBoundary>
            <div className="dashboard-container">
                <div className="header">
                    <h1>Analysis Workstation</h1>
                    <button onClick={logout} className="btn-logout">
                        Logout
                    </button>
                </div>

                <div className="tabs">
                    <button
                        onClick={() => setActiveTab('upload')}
                        className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
                    >
                        Data Input
                    </button>
                    <button
                        onClick={() => setActiveTab('charts')}
                        className={`tab-btn ${activeTab === 'charts' ? 'active' : ''}`}
                        disabled={!datasetId}
                    >
                        Visualization
                    </button>
                    <button
                        onClick={() => setActiveTab('compare')}
                        className={`tab-btn ${activeTab === 'compare' ? 'active' : ''}`}
                    >
                        Compare
                    </button>
                    <button
                        onClick={() => setActiveTab('history')}
                        className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
                    >
                        Experiment Log
                    </button>
                </div>

                <div className="content-area">
                    {activeTab === 'upload' && <Upload onUploadSuccess={handleUploadSuccess} />}
                    {activeTab === 'charts' && <Charts datasetId={datasetId} />}
                    {activeTab === 'compare' && <Compare />}
                    {activeTab === 'history' && <History refreshTrigger={datasetId} />}
                </div>
            </div>
        </ErrorBoundary>
    );
};

export default Dashboard;
