import { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { uploadCSV } from '../services/api';
import Papa from 'papaparse';

const REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'];

const Upload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [previewError, setPreviewError] = useState('');
    const [isDragging, setIsDragging] = useState(false);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');
    const { token, logout } = useAuth();
    const fileInputRef = useRef(null);

    const MAX_SIZE = 10 * 1024 * 1024;

    const validateAndPreview = (selectedFile) => {
        setError('');
        setStats(null);
        setPreview(null);
        setPreviewError('');

        if (!selectedFile.name.toLowerCase().endsWith('.csv')) {
            setPreviewError('Invalid file type. Please select a .csv file.');
            return;
        }

        if (selectedFile.size > MAX_SIZE) {
            setPreviewError(`File too large. Max size is ${MAX_SIZE / (1024 * 1024)}MB.`);
            return;
        }

        setFile(selectedFile);

        Papa.parse(selectedFile, {
            header: true,
            preview: 5,
            skipEmptyLines: true,
            complete: (results) => {
                if (!results.data || results.data.length === 0) {
                    setPreviewError('CSV file appears to be empty. Please add data rows.');
                    return;
                }

                const columns = results.meta.fields || [];
                const missingCols = REQUIRED_COLUMNS.filter(col => !columns.includes(col));
                const extraCols = columns.filter(col => !REQUIRED_COLUMNS.includes(col));

                if (missingCols.length > 0) {
                    setPreviewError(`Missing columns: ${missingCols.join(', ')}. Required: ${REQUIRED_COLUMNS.join(', ')}`);
                    return;
                }

                if (extraCols.length > 0) {
                    setPreviewError(`Unexpected columns: ${extraCols.join(', ')}. Only these are allowed: ${REQUIRED_COLUMNS.join(', ')}`);
                    return;
                }

                setPreview({ columns, rows: results.data });
            },
            error: () => {
                setPreviewError('Failed to parse CSV file. Please check file format.');
            }
        });
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            validateAndPreview(selectedFile);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            validateAndPreview(droppedFile);
        }
    };

    const handleZoneClick = () => {
        fileInputRef.current?.click();
    };

    const handleUpload = async () => {
        if (!file) return;

        setError('');
        setStats(null);
        setLoading(true);

        try {
            const data = await uploadCSV(file, token);
            setStats(data);
            setPreview(null);
            setFile(null);
            if (onUploadSuccess && data.id) {
                onUploadSuccess(data.id);
            }
        } catch (err) {
            if (err.message === 'Unauthorized') {
                logout();
                return;
            }
            setError(err.message || 'Upload failed. Please check file format and try again.');
        } finally {
            setLoading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleCancel = () => {
        setFile(null);
        setPreview(null);
        setPreviewError('');
        if (fileInputRef.current) fileInputRef.current.value = '';
    };

    const dropZoneClass = `drop-zone ${isDragging ? 'drag-over' : ''} ${file && preview ? 'has-file' : ''}`;

    return (
        <div className="upload-section">
            <h3>Data Acquisition</h3>

            <div
                className={dropZoneClass}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleZoneClick}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />
                {file ? (
                    <div className="drop-zone-content">
                        <span className="file-icon">📄</span>
                        <span className="file-name">{file.name}</span>
                        <span className="file-size">({(file.size / 1024).toFixed(1)} KB)</span>
                    </div>
                ) : (
                    <div className="drop-zone-content">
                        <span className="drop-icon">⬆</span>
                        <span>Drop CSV here or click to browse</span>
                    </div>
                )}
            </div>

            {previewError && (
                <div className="alert alert-error">
                    <strong>Validation Error:</strong> {previewError}
                    <div className="error-help">Reference: sample_equipment_data.csv</div>
                </div>
            )}

            {preview && (
                <div className="preview-section">
                    <div className="preview-header">
                        <h4>Preview (first {preview.rows.length} rows)</h4>
                        <span className="preview-valid">✓ Columns validated</span>
                    </div>
                    <div className="table-container">
                        <table className="table preview-table">
                            <thead>
                                <tr>
                                    {preview.columns.map(col => (
                                        <th key={col}>{col}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {preview.rows.map((row, i) => (
                                    <tr key={i}>
                                        {preview.columns.map(col => (
                                            <td key={col}>{row[col]}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="preview-actions">
                        <button onClick={handleCancel} className="btn-secondary">
                            Cancel
                        </button>
                        <button
                            onClick={handleUpload}
                            disabled={loading}
                            className="btn-primary"
                        >
                            {loading ? 'Processing...' : 'Analyze'}
                        </button>
                    </div>
                </div>
            )}

            {error && <div className="alert alert-error">Error: {error}</div>}

            {stats && (
                <div className="alert alert-success">
                    <div className="stats-display">
                        <h4>Analysis Complete</h4>
                        <div className="stat-row">
                            <span className="stat-label">Total Records</span>
                            <span className="stat-value">{stats.total_count}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Flowrate</span>
                            <span className="stat-value">{Number(stats.avg_flowrate).toFixed(2)}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Pressure</span>
                            <span className="stat-value">{Number(stats.avg_pressure).toFixed(2)}</span>
                        </div>
                        <div className="stat-row">
                            <span className="stat-label">Avg Temperature</span>
                            <span className="stat-value">{Number(stats.avg_temperature).toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Upload;
