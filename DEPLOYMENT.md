# Deployment & Distribution Guide

This document outlines the standard operating procedures for deploying the Chemical Equipment Parameter Visualizer across its hybrid architecture.

## 1. System Components & Strategy

The system relies on a **Hub-and-Spoke** architecture:
*   **Central Backend**: Django REST API hosted on Render (Free Tier).
*   **Web Client**: React/Vite application hosted on Vercel.
*   **Desktop Client**: Python/PyQt5 executable distributed via GitHub Releases.

---

## 2. Environment Configuration

The application requires specific environment variables for security and connectivity.

### Backend (Render)
| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `SECRET_KEY` | Cryptographic key for Django. | `django-insecure-...` (Use a strong generated string in production) |
| `DEBUG` | Toggle debug mode. | `False` (Must be False in production) |
| `ALLOWED_HOSTS` | Whitelist of host/domain names. | `*` or `your-app.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | Whitelist of client origins. | `https://your-frontend.vercel.app` |
| `RENDER` | Signals Render environment. | `true` |

### Frontend (Vercel)
| Variable | Description | Value |
| :--- | :--- | :--- |
| `VITE_API_URL` | Base URL of the live backend. | `https://your-app-name.onrender.com/api` |

---

## 3. Backend Deployment (Render)

We use Render's Python/Django runtime.

1.  **Service Creation**:
    *   Initialize a new **Web Service** connected to this repository.
    *   **Root Directory**: `backend`
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
    *   **Start Command**: `gunicorn config.wsgi:application`

2.  **Persistence Strategy (SQLite):**
    *   **Ephemeral (Free Tier)**: Filesystem resets on deploy. Data is lost.
    *   **Persistent (Paid/Disk)**: Attach a disk to `/var/lib/data` and ensure your `settings.py` reads `RENDER` env var to switch DB paths.

---

## 4. Frontend Deployment (Vercel)

We use Vercel for high-performance static hosting.

1.  **Project Import**:
    *   Import repository to Vercel.
    *   **Framework Preset**: Vite
    *   **Root Directory**: `web`
2.  **Build Configuration**:
    *   **Build Command**: `npm run build`
    *   **Output Directory**: `dist`
3.  **Routing**:
    *   Ensure `vercel.json` dictates rewrites to `index.html` for client-side routing.

---

## 5. Desktop Client Distribution

The desktop client allows a native experience without a browser wrapper.

### Building the Executable (Windows)
1.  Navigate to the `desktop/` directory.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run PyInstaller:
    ```bash
    pyinstaller --noconsole --onefile --name="ChemicalVisualizer" main.py
    ```
4.  The artifact `ChemicalVisualizer.exe` will be generated in `dist/`.

### Releasing
1.  Create a **GitHub Release** (e.g., `v1.0.0`).
2.  Attach `ChemicalVisualizer.exe` as a binary asset.
3.  Users can download and run this directly.

---

## 6. Verification Protocol

After deployment, perform these standard checks:

1.  **API Health**: `GET /api/health/` -> Returns `200 OK`.
2.  **Authentication**: Register a new user and login.
3.  **Cross-Origin Resource Sharing (CORS)**: Verify the Web App can fetch data from the Backend.
4.  **End-to-End Flow**: Upload a valid CSV and generate a PDF Report.
