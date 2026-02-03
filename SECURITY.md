# Security Policy

## Authentication Overview

The Chemical Equipment Parameter Visualizer implements a strict **Token-Based Authentication** model using Django REST Framework (DRF).

*   **Type**: Token Auth (DRF Default).
*   **Scope**: Global. All data modification/retrieval endpoints require a valid token in the header.
    ```http
    Authorization: Token <your_generated_token>
    ```
*   **Isolation**: We implement **Row-Level Security** at the View layer. All database queries are filtered by `request.user` (e.g., `EquipmentDataset.objects.filter(user=request.user)`). This guarantees that user A can strictly never access user B's data.

## Known Security Limitations

### Security Constraints

1.  **Permanent Tokens**: Tokens do not expire. In a real-world scenario, this poses a risk if a token is leaked.
2.  **No Refresh Flow**: There is no refresh token mechanism.
3.  **SQLite Encryption**: Data is stored in a standard SQLite file without encryption-at-rest.

## What is NOT Implemented

*   **Multi-Factor Authentication (MFA)**: Not required for this scope.
*   **Role-Based Access Control (RBAC)**: All users have equal "User" level permissions. There are no Admin/Manager roles exposed to the frontend.

## Production Hardening Recommendations

To move this system to a high-security production environment, we recommend:

1.  **Switch to JWT**: Migrate from DRF Token Auth to `SimpleJWT` for short-lived access tokens and secure refresh rotation.
2.  **Database Upgrade**: Migrate from SQLite to **PostgreSQL** with TDE (Transparent Data Encryption) enabled.
3.  **HTTPS Enforcement**: Ensure strict HSTS and SSL/TLS termination at the load balancer level (handled by Render automatically).
4.  **Rate Limiting**: Implement Redis-based throttling for the `/upload/` endpoint to prevent DoS attacks.
