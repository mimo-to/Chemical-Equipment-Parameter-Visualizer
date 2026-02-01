import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getHistory, compareDatasets, getVisualization } from '../services/api';
import {
    Chart as ChartJS,
    CategoryScale, LinearScale, BarElement,
    Title, Tooltip, Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const COLORS = ['#00b4d8', '#06ffa5', '#ffd60a'];
const FONT = { family: "'JetBrains Mono', monospace", size: 11 };

const Compare = () => {
    const [history, setHistory] = useState([]);
    const [selected1, setSelected1] = useState('');
    const [selected2, setSelected2] = useState('');
    const [comparison, setComparison] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { token } = useAuth();

    useEffect(() => {
        getHistory(token)
            .then(setHistory)
            .catch(() => setError('Failed to load datasets'));
    }, [token]);

    const handleCompare = async () => {
        if (!selected1 || !selected2) return;
        if (selected1 === selected2) {
            setError('Select two different datasets');
            return;
        }

        setLoading(true);
        setError('');
        try {
            const [result, viz1, viz2] = await Promise.all([
                compareDatasets(selected1, selected2, token),
                getVisualization(selected1, token),
                getVisualization(selected2, token)
            ]);
            setComparison({ ...result, viz1, viz2 });
        } catch (err) {
            setError('Comparison failed');
        } finally {
            setLoading(false);
        }
    };

    const barOpts = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { color: 'rgba(0,119,182,0.2)' }, ticks: { font: FONT } },
            y: { grid: { color: 'rgba(0,119,182,0.2)' }, ticks: { font: FONT } }
        }
    };

    const buildBarData = (viz, label) => ({
        labels: viz.averages.labels,
        datasets: [{
            label,
            data: viz.averages.data,
            backgroundColor: COLORS,
            borderRadius: 2
        }]
    });

    return (
        <div className="compare-section">
            <h3>Dataset Comparison</h3>

            <div className="compare-selectors">
                <div className="selector-group">
                    <label>Dataset A</label>
                    <select
                        value={selected1}
                        onChange={(e) => setSelected1(e.target.value)}
                        className="compare-select"
                    >
                        <option value="">Select dataset...</option>
                        {history.map(item => (
                            <option key={item.id} value={item.id}>
                                {item.filename}
                            </option>
                        ))}
                    </select>
                </div>

                <span className="vs-label">VS</span>

                <div className="selector-group">
                    <label>Dataset B</label>
                    <select
                        value={selected2}
                        onChange={(e) => setSelected2(e.target.value)}
                        className="compare-select"
                    >
                        <option value="">Select dataset...</option>
                        {history.map(item => (
                            <option key={item.id} value={item.id}>
                                {item.filename}
                            </option>
                        ))}
                    </select>
                </div>

                <button
                    onClick={handleCompare}
                    disabled={!selected1 || !selected2 || loading}
                    className="btn-primary"
                >
                    {loading ? 'Comparing...' : 'Compare'}
                </button>
            </div>

            {error && <p className="alert alert-error">{error}</p>}

            {comparison && (
                <div className="comparison-results">
                    <div className="diff-summary">
                        <h4>Difference (A - B)</h4>
                        <div className="diff-grid">
                            <div className="diff-card">
                                <span className="diff-label">Flowrate</span>
                                <span className={`diff-value ${comparison.comparison.flowrate_diff >= 0 ? 'positive' : 'negative'}`}>
                                    {comparison.comparison.flowrate_diff >= 0 ? '+' : ''}{comparison.comparison.flowrate_diff}
                                </span>
                            </div>
                            <div className="diff-card">
                                <span className="diff-label">Pressure</span>
                                <span className={`diff-value ${comparison.comparison.pressure_diff >= 0 ? 'positive' : 'negative'}`}>
                                    {comparison.comparison.pressure_diff >= 0 ? '+' : ''}{comparison.comparison.pressure_diff}
                                </span>
                            </div>
                            <div className="diff-card">
                                <span className="diff-label">Temperature</span>
                                <span className={`diff-value ${comparison.comparison.temperature_diff >= 0 ? 'positive' : 'negative'}`}>
                                    {comparison.comparison.temperature_diff >= 0 ? '+' : ''}{comparison.comparison.temperature_diff}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="side-by-side">
                        <div className="compare-chart">
                            <h4>{comparison.dataset1.filename}</h4>
                            <div className="chart-wrapper">
                                <Bar data={buildBarData(comparison.viz1, 'Dataset A')} options={barOpts} />
                            </div>
                        </div>
                        <div className="compare-chart">
                            <h4>{comparison.dataset2.filename}</h4>
                            <div className="chart-wrapper">
                                <Bar data={buildBarData(comparison.viz2, 'Dataset B')} options={barOpts} />
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {history.length < 2 && (
                <p className="empty-state">Upload at least 2 datasets to compare.</p>
            )}
        </div>
    );
};

export default Compare;
