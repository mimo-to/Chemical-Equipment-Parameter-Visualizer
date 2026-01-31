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

ChartJS.defaults.color = '#caf0f8';
ChartJS.defaults.borderColor = '#0077b6';

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
            } catch (err) {
                setError('Failed to load chart data');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [datasetId, token]);

    if (!datasetId) return null;
    if (loading) return <p className="loading-state">Loading visualization data...</p>;
    if (error) return <p className="alert alert-error">{error}</p>;
    if (!chartData) return null;

    const { type_distribution, averages } = chartData;

    const pieData = {
        labels: type_distribution.labels,
        datasets: [{
            label: 'Equipment Count',
            data: type_distribution.data,
            backgroundColor: [
                '#00b4d8',
                '#06ffa5',
                '#ffd60a',
                '#0077b6',
                '#90e0ef',
                '#48cae4',
                '#023e8a',
                '#caf0f8',
                '#ade8f4',
                '#03045e',
            ],
            borderWidth: 0,
        }],
    };

    const barData = {
        labels: averages.labels,
        datasets: [{
            label: 'Average Values',
            data: averages.data,
            backgroundColor: [
                '#00b4d8',
                '#06ffa5',
                '#ffd60a',
            ],
            borderRadius: 2,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: { family: "'JetBrains Mono', monospace", size: 11 },
                    padding: 16,
                }
            },
            title: { display: false },
        },
        scales: {
            x: {
                grid: { color: 'rgba(0, 119, 182, 0.2)' },
                ticks: { font: { family: "'JetBrains Mono', monospace", size: 10 } }
            },
            y: {
                grid: { color: 'rgba(0, 119, 182, 0.2)' },
                ticks: { font: { family: "'JetBrains Mono', monospace", size: 10 } }
            }
        }
    };

    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: { family: "'JetBrains Mono', monospace", size: 11 },
                    padding: 12,
                }
            },
        },
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
                    <div className="chart-wrapper">
                        <Pie data={pieData} options={pieOptions} />
                    </div>
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">Average Parameters</h3>
                    <div className="chart-wrapper">
                        <Bar data={barData} options={options} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Charts;
