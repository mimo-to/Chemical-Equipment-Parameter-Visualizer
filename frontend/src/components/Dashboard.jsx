import { useState } from 'react';
import Upload from './Upload';
import Charts from './Charts';
import History from './History';

const Dashboard = () => {
    const [datasetId, setDatasetId] = useState(null);

    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome to the protected dashboard.</p>
            <Upload onUploadSuccess={setDatasetId} />
            <Charts datasetId={datasetId} />
            <History refreshTrigger={datasetId} />
        </div>
    );
};

export default Dashboard;
