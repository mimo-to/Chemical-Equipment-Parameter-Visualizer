# Deployment Guide

## 1. Environment Variables

### Backend (Render/Production)
Set these environment variables in your deployment platform:

*   `SECRET_KEY`: Generate a strong random string (e.g., using `openssl rand -base64 32`).
*   `DEBUG`: `False`
*   `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (e.g., `your-app-name.onrender.com,api.yourdomain.com`).
*   `CORS_ALLOWED_ORIGINS`: Comma-separated list of frontend origins (e.g., `https://your-frontend-app.vercel.app,http://localhost:5173`).
*   `DATABASE_URL`: (Optional) Connection string if using PostgreSQL.
*   `RENDER`: `true` (This triggers the use of the persistent SQLite disk at `/var/lib/data/db.sqlite3`).
*   `SECURE_SSL_REDIRECT`: `True` (Recommended for production).
*   `SESSION_COOKIE_SECURE`: `True` (Recommended).
*   `CSRF_COOKIE_SECURE`: `True` (Recommended).

### Frontend (Vercel/Netlify)
Set this environment variable:

*   `VITE_API_URL`: The full URL of your deployed backend API (e.g., `https://your-app-name.onrender.com/api`).

## 2. Render Deployment (Backend)

1.  **Create a New Web Service** on Render connected to your GitHub repository.
2.  **Settings:**
    *   **Runtime:** Python 3
    *   **Build Command:** `./build.sh`
    *   **Start Command:** `cd backend && gunicorn config.wsgi:application`
    *   **Start Command:** `cd backend && gunicorn config.wsgi:application`
    *   **Environment Variables:** Add all variables from the "Environment Variables" section above.

3.  **Database Persistence (Crucial Step):**
    *   **Free Tier (Ephemeral):** By default, Render's free tier has an "ephemeral" filesystem. This means **all data (users, datasets) will be deleted** whenever the server restarts or redeploys. This is acceptable for a portfolio demo to show functionality.
    *   **Paid Tier (Persistent):** To save data permanently:
        1.  Go to your Render Dashboard > Disks.
        2.  Create a new Disk named `data` with mount path `/var/lib/data`.
        3.  Attach it to your Web Service.
        4.  Ensure the `RENDER` environment variable is set to `true`.
        5.  The application will automatically detect the disk and save `db.sqlite3` there.

## 3. Vercel Deployment (Frontend)

1.  **Import Project** in Vercel.
2.  **Framework Preset:** Vite
3.  **Root Directory:** `web`
4.  **Build Command:** `npm run build`
5.  **Output Directory:** `dist`
6.  **Environment Variables:** Add `VITE_API_URL` pointing to your Render backend (e.g., `https://your-app.onrender.com/api`).
7.  **Rewrites (IMPORTANT):**
    *   Ensure a `vercel.json` exists in the `web` directory to handle React routing.
    *   If missing, create it with:
        ```json
        {
          "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
        }
        ```

## 4. Post-Deployment Verification

1.  **Health Check:** Visit `https://your-backend-url/api/health/`. You should see `{"status": "ok"}`.
    *   *Note: The trailing slash / is important for Django.*
2.  **User Registration:** Try to register a new user in the deployed app.
3.  **Desktop App Download:** Verify the download button on the Login page works and downloads the `.zip` or `.exe`.
4.  **Data Persistence Test:** 
    *   Upload a file.
    *   In Render Dashboard, manually "Restart Service".
    *   If on Free Tier: Data should be gone (Normal).
    *   If using Disk: Data should persist.
