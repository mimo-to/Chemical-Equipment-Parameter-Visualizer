# Chemical Equipment Parameter Visualizer

A full-stack application for visualizing and analyzing chemical equipment parameters (Flowrate, Pressure, Temperature). It features a secure backend, a modern web dashboard, and a native desktop application.

## Tech Stack

*   **Backend**: Django, Django REST Framework (DRF), Pandas, SQLite
*   **Web Frontend**: React, Vite, Chart.js, Tailwind CSS
*   **Desktop App**: PyQt5, Matplotlib
*   **Database**: SQLite

## Repository Structure

*   `backend/` - Django project and API source code
*   `web/` - React Web Application source code
*   `desktop/` - PyQt5 Desktop Application source code
*   `sample_equipment_data.csv` - Sample dataset for testing application features

## Backend Setup

1.  **Prerequisites**: Python 3.8 or higher
2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
3.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # macOS/Linux
    # source venv/bin/activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Initialize the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```
    The server will start at `http://127.0.0.1:8000`.

## Creating Users

The application requires authenticated users. Create a user account using Django's management command:

```bash
cd backend
python manage.py createsuperuser
```

Follow the prompts to create a username and password. This account can be used to log in to both the web and desktop applications.

**For Quick Testing (Demo Credentials):**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_user(username='demo', password='demo123')
exit()
```

## Important Configuration Notes

**Backend URL:** Both the web and desktop applications are configured to connect to the backend at `http://127.0.0.1:8000`. Ensure the Django development server is running at this address before launching either frontend.

**CORS Configuration:** The backend is pre-configured to accept requests from `http://localhost:5173` (Vite default) and `http://localhost:3000`. If you change frontend ports, update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`.


## Web Frontend Setup

1.  **Prerequisites**: Node.js 18+ (Recommended) or 16+
2.  **Navigate to the web directory**:
    ```bash
    cd web
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Run the development server**:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

## Desktop App Setup

1.  **Prerequisites**: Python 3.8 or higher. Ensure the backend server is running first.
2.  **Navigate to the desktop directory**:
    ```bash
    cd desktop
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application**:
    ```bash
    python main.py
    ```

## API Reference

The following endpoints are available for integration:

| Method | Endpoint | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/login/` | Obtain Authentication Token | None |
| `POST` | `/api/upload/` | Upload CSV & Parse Data | Token Required |
| `GET` | `/api/history/` | Retrieve list of uploaded datasets | Token Required |
| `GET` | `/api/report/<id>/`| Download Stats Report as PDF | Token Required |

## Usage Instructions

1.  **Start the Backend**: Run `python manage.py runserver` in the backend directory.
2.  **Login**:
    *   **Web Interface**: Open `http://localhost:5173`. You can create a new account or log in with existing credentials.
    *   **Desktop Interface**: Run `python main.py` and enter your credentials.
3.  **Upload Data**:
    *   Use the `sample_equipment_data.csv` file provided in the root directory.
    *   Click "Upload" to submit the file for processing.
4.  **Analyze**:
    *   The application will automatically generate charts (Type Distribution and Average Parameters).
    *   Statistical summaries will be displayed on the dashboard.
5.  **History & Reports**:
    *   Navigate to the "History" section.
    *   Select a previously uploaded dataset.
    *   Click "Save PDF" or "Download Report" to export the analysis.
