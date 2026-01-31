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
        console.error("System error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-panel">
                    <h2>System Malfunction</h2>
                    <p>{this.state.error && this.state.error.toString()}</p>
                    <button onClick={() => window.location.reload()}>
                        Restart System
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
