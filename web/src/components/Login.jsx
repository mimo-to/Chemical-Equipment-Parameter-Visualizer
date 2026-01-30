import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser } from '../services/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login, isAuthenticated } = useAuth();
    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/');
        }
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        console.log(`[Login] Attempting login for user: ${username}`);
        try {
            const data = await loginUser(username, password);
            login(data.token);
            console.log('[Login] Success');
        } catch (err) {
            console.error('[Login] Failed:', err.message);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', width: '100%', background: '#f0f2f5', margin: 0 }}>
            <div style={{ padding: '40px', border: '1px solid #ccc', borderRadius: '8px', width: '300px', background: 'white', display: 'flex', flexDirection: 'column', gap: '15px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                <h2 style={{ textAlign: 'center', margin: '0 0 20px 0', color: '#333' }}>Login</h2>
                {error && <div style={{ background: '#f8d7da', color: '#721c24', padding: '10px', borderRadius: '4px', textAlign: 'center', fontSize: '0.9rem' }}>{error}</div>}
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                        <label style={{ fontSize: '0.9rem', color: '#666' }}>Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ddd', fontSize: '1rem' }}
                            required
                            disabled={loading}
                        />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', position: 'relative' }}>
                        <label style={{ fontSize: '0.9rem', color: '#666' }}>Password</label>
                        <input
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ddd', fontSize: '1rem', width: '100%', boxSizing: 'border-box' }}
                            required
                            disabled={loading}
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            disabled={loading}
                            style={{
                                position: 'absolute',
                                right: '10px',
                                top: '32px',
                                background: 'none',
                                border: 'none',
                                cursor: 'pointer',
                                fontSize: '12px',
                                color: '#007bff'
                            }}
                        >
                            {showPassword ? "Hide" : "Show"}
                        </button>
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            padding: '12px',
                            background: loading ? '#6c757d' : '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            fontSize: '1rem',
                            fontWeight: 'bold',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Signing In...' : 'Login'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
