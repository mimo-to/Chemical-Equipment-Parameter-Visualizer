import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught an error", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '20px', border: '1px solid red', margin: '20px', borderRadius: '5px' }}>
                    <h2 style={{ color: 'red' }}>Something went wrong.</h2>
                    <p>{this.state.error && this.state.error.toString()}</p>
                    <button onClick={() => window.location.reload()}>Reload Page</button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
