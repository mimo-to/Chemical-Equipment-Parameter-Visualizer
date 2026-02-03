import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser, registerUser, checkHealth } from '../services/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [isRegistering, setIsRegistering] = useState(false);
    const { login, isAuthenticated } = useAuth();
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);

    useEffect(() => {
        checkHealth().catch(() => {
            console.log('Server warming ping sent');
        });
    }, []);

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/');
        }
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const data = isRegistering
                ? await registerUser(username, password, email)
                : await loginUser(username, password);
            login(data.token);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setIsRegistering(!isRegistering);
        setError('');
    };

    return (
        <div className="login-page">
            <div className="login-card">
                <div className="login-header">
                    <h2 className="login-title">CHEM-VIS</h2>
                    <p className="login-subtitle">{isRegistering ? 'Create Account' : 'Authentication Required'}</p>
                </div>

                <div className="mb-4 px-3 py-2 rounded text-center" style={{ border: '1px solid rgba(0, 180, 216, 0.2)' }}>
                    <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--text-muted)', margin: 0, letterSpacing: '0.5px' }}>
                        <span style={{ color: 'var(--warning)', marginRight: '6px' }}>⚠ NOTICE:</span>
                        IF UNRESPONSIVE, PLEASE WAIT <span style={{ color: 'var(--text-main)', fontWeight: 'bold' }}>~50s</span> FOR SERVER WAKE-UP.
                    </p>
                </div>

                {error && <div className="login-error">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            disabled={loading}
                            autoComplete="username"
                        />
                    </div>

                    {isRegistering && (
                        <div className="form-group">
                            <label className="form-label">Email (optional)</label>
                            <input
                                type="email"
                                className="form-input"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={loading}
                                autoComplete="email"
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label">Password {isRegistering && '(min 8 chars)'}</label>
                        <div className="password-wrapper">
                            <input
                                type={showPassword ? "text" : "password"}
                                className="form-input"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                disabled={loading}
                                autoComplete={isRegistering ? "new-password" : "current-password"}
                            />
                            <button
                                type="button"
                                className="btn-toggle"
                                onClick={() => setShowPassword(!showPassword)}
                                disabled={loading}
                            >
                                {showPassword ? "Hide" : "Show"}
                            </button>
                        </div>
                    </div>

                    <button type="submit" className="btn-submit" disabled={loading}>
                        {loading ? (isRegistering ? 'Creating...' : 'Authenticating...') : (isRegistering ? 'Create Account' : 'Access System')}
                    </button>
                </form>

                <div className="login-toggle">
                    <button type="button" className="btn-link" onClick={toggleMode} disabled={loading}>
                        {isRegistering ? 'Already have an account? Sign In' : 'Need an account? Sign Up'}
                    </button>
                </div>

                <div className="download-msg">
                    <a
                        href="/Chemical-Equipment-Parameter-Visualizer.zip"
                        download
                        className="btn-download"
                    >
                        <span>⬇️</span> Download Desktop Client (.zip)
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Login;
