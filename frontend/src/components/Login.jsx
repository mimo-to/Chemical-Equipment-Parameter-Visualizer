import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser } from '../services/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
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
        setError('');
        try {
            const data = await loginUser(username, password);
            login(data.token);
            // Navigation handled by useEffect
        } catch (err) {
            setError('Invalid credentials');
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
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
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
                        style={{ padding: '12px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem', fontWeight: 'bold' }}
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
