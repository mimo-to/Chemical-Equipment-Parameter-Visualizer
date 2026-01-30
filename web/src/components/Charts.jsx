import { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { useAuth } from '../context/AuthContext';
import { getVisualization } from '../services/api';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

ChartJS.defaults.color = '#f8fafc';
ChartJS.defaults.borderColor = '#334155';

const Charts = ({ datasetId }) => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { token } = useAuth();

    useEffect(() => {
        if (!datasetId) return;

        const fetchData = async () => {
            setLoading(true);
            try {
                const data = await getVisualization(datasetId, token);
                setChartData(data);
                setError('');
            } catch (err) {
                setError('Failed to load charts');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [datasetId, token]);

    if (!datasetId) return null;
    if (loading) return <p>Loading charts...</p>;
    if (error) return <p className="alert alert-error">{error}</p>;
    if (!chartData) return null;

    const { type_distribution, averages } = chartData;

    const pieData = {
        labels: type_distribution.labels,
        datasets: [
            {
                label: 'Equipment Count',
                data: type_distribution.data,
                backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6',
                    '#ec4899',
                    '#06b6d4',
                    '#f97316',
                    '#6366f1',
                    '#14b8a6',
                ],
                borderWidth: 0,
            },
        ],
    };

    const barData = {
        labels: averages.labels,
        datasets: [
            {
                label: 'Average Values',
                data: averages.data,
                backgroundColor: [
                    '#3b82f6',
                    '#f59e0b',
                    '#ef4444',
                ],
                borderRadius: 4,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'bottom' },
            title: { display: false },
        },
    };

    return (
        <div style={{ marginTop: '30px', display: 'flex', gap: '30px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <div className="chart-container">
                <h3 style={{ textAlign: 'center', marginBottom: '20px', color: '#f8fafc' }}>Equipment Type Distribution</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                    <Pie data={pieData} options={options} />
                </div>
            </div>
            <div className="chart-container">
                <h3 style={{ textAlign: 'center', marginBottom: '20px', color: '#f8fafc' }}>Average Parameters</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                    <Bar data={barData} options={options} />
                </div>
            </div>
        </div>
    );
};

export default Charts;
