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
    if (error) return <p style={{ color: 'red' }}>{error}</p>;
    if (!chartData) return null;

    const { type_distribution, averages } = chartData;

    const pieData = {
        labels: type_distribution.labels,
        datasets: [
            {
                label: 'Equipment Count',
                data: type_distribution.data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                ],
                borderWidth: 1,
            },
        ],
    };

    const barData = {
        labels: averages.labels,
        datasets: [
            {
                label: 'Average Values',
                data: averages.data,
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
            },
        ],
    };

    return (
        <div style={{ marginTop: '30px', display: 'flex', gap: '30px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <div style={{ flex: '1 1 400px', minWidth: '300px', padding: '20px', background: 'white', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>Equipment Type Distribution</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                    <Pie data={pieData} options={{ maintainAspectRatio: false }} />
                </div>
            </div>
            <div style={{ flex: '1 1 500px', minWidth: '300px', padding: '20px', background: 'white', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>Average Parameters</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                    <Bar options={{ responsive: true, maintainAspectRatio: false }} data={barData} />
                </div>
            </div>
        </div>
    );
};

export default Charts;
