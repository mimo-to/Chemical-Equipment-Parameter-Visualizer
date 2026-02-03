# Security Policy

## Authentication Model

The Chemical Equipment Parameter Visualizer uses **Token-Based Authentication** powered by the Django REST Framework (DRF).

*   **Mechanism**: Every request to a protected endpoint must include the `Authorization` header.
    ```http
    Authorization: Token <your_generated_token>
    ```
*   **User Isolation**: All data endpoints (`/history`, `/report`, etc.) are filtered by `request.user`. A user strictly cannot access, view, or compare datasets belonging to another user.

## Known Limitations

### 1. Token Expiry
*   Current implementation uses permanent tokens for simplicity in this demo environment.
*   **Recommendation for Production**: Implement JWT (JSON Web Tokens) with short-lived access tokens and refresh tokens.

### 2. Rate Limiting
*   **Current User Upload Limit**: 10 requests / minute.
*   **Global Rate Limits**: Not currently configured for Nginx/Load Balancer level.

### 3. Database Encryption
*   **Storage**: Data is stored in a standard SQLite file.
*   **Implication**: This is acceptable for a demo/student project but strictly **not** recommended for production storing sensitive industrial data.
*   **Recommendation**: Use PostgreSQL with encryption-at-rest (TDE) for production.

## Reporting Vulnerabilities

This is an academic/internship submission. If you discover a security vulnerability, please open an issue in the repository.
