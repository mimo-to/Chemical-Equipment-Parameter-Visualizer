import { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale, LinearScale, BarElement,
    Title, Tooltip, Legend, ArcElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { useAuth } from '../context/AuthContext';
import { getVisualization } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);
ChartJS.defaults.color = '#caf0f8';
ChartJS.defaults.borderColor = '#0077b6';

const COLORS = ['#00b4d8', '#06ffa5', '#ffd60a', '#0077b6', '#90e0ef', '#48cae4', '#023e8a'];
const FONT = { family: "'JetBrains Mono', monospace", size: 11 };

const Charts = ({ datasetId }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { token } = useAuth();

    useEffect(() => {
        if (!datasetId) return;
        setLoading(true);
        getVisualization(datasetId, token)
            .then(setData)
            .catch(() => setError('Failed to load chart data'))
            .finally(() => setLoading(false));
    }, [datasetId, token]);

    if (!datasetId) return null;
    if (loading) return <p className="loading-state">Loading visualization data...</p>;
    if (error) return <p className="alert alert-error">{error}</p>;
    if (!data) return null;

    const { type_distribution, averages } = data;

    const pieConfig = {
        labels: type_distribution.labels,
        datasets: [{ data: type_distribution.data, backgroundColor: COLORS, borderWidth: 0 }]
    };

    const barConfig = {
        labels: averages.labels,
        datasets: [{ data: averages.data, backgroundColor: COLORS.slice(0, 3), borderRadius: 2 }]
    };

    const baseOpts = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom', labels: { font: FONT, padding: 14 } } }
    };

    const barOpts = {
        ...baseOpts,
        scales: {
            x: { grid: { color: 'rgba(0,119,182,0.2)' }, ticks: { font: FONT } },
            y: { grid: { color: 'rgba(0,119,182,0.2)' }, ticks: { font: FONT } }
        }
    };

    return (
        <div className="charts-section">
            <div className="stats-summary">
                <h3>Parameter Averages</h3>
                <div className="stats-grid">
                    {averages.labels.map((label, i) => (
                        <div key={label} className="stat-card">
                            <span className="stat-label">{label}</span>
                            <span className="stat-value">{Number(averages.data[i]).toFixed(2)}</span>
                        </div>
                    ))}
                </div>
            </div>
            <div className="charts-grid">
                <div className="chart-container">
                    <h3 className="chart-title">Equipment Type Distribution</h3>
                    <div className="chart-wrapper"><Pie data={pieConfig} options={baseOpts} /></div>
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">Average Parameters</h3>
                    <div className="chart-wrapper"><Bar data={barConfig} options={barOpts} /></div>
                </div>
            </div>
        </div>
    );
};

export default Charts;
