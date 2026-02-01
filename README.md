# Chemical Equipment Parameter Visualizer

A full-stack data visualization platform for chemical engineering applications. Upload CSV datasets containing equipment parameters and instantly generate interactive visualizations, statistical summaries, and downloadable PDF reports.

Built for the FOSSEE Semester Internship 2026 screening project.

---

## Features

- **CSV Upload & Validation** - Upload equipment data with automatic format validation
- **Interactive Charts** - Pie charts for equipment type distribution, bar charts for parameter averages
- **Statistical Analysis** - Calculate averages, min/max values for Flowrate, Pressure, and Temperature
- **Dataset History** - Access your last 5 uploaded datasets
- **PDF Reports** - Generate and download professional analysis reports
- **Dual Frontend** - Modern web dashboard + native desktop application
- **Token Authentication** - Secure API access with token-based auth

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.2, Django REST Framework, Pandas |
| **Web Frontend** | React 18, Vite, Chart.js, Tailwind CSS |
| **Desktop App** | PyQt5, Matplotlib |
| **Database** | SQLite |
| **PDF Generation** | ReportLab |

---

## Project Structure

```
Chemical-Equipment-Parameter-Visualizer/
├── backend/                 # Django REST API
│   ├── api/                 # Core API app
│   │   ├── views.py         # API endpoints
│   │   ├── models.py        # Dataset model
│   │   ├── validators.py    # CSV validation logic
│   │   └── tests/           # Unit tests
│   └── config/              # Django settings
├── web/                     # React Web Application
│   └── src/
│       ├── components/      # React components
│       └── App.jsx          # Main application
├── desktop/                 # PyQt5 Desktop Application
│   ├── main.py              # Entry point
│   ├── main_window.py       # Main window
│   ├── charts_widget.py     # Visualization widget
│   └── theme.py             # Dark theme styling
├── sample_equipment_data.csv # Sample dataset for testing
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ (for web frontend)

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at `http://127.0.0.1:8000`

### 2. Create User Account

```bash
python manage.py createsuperuser
```

**Quick Demo User:**
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('demo', password='demo123')"
```

### 3. Web Frontend Setup

```bash
cd web
npm install
npm run dev
```

Web app runs at `http://localhost:5173`

### 4. Desktop App Setup

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

---

## API Reference

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/login/` | Get authentication token | No |
| `POST` | `/api/upload/` | Upload CSV dataset | Token |
| `GET` | `/api/history/` | List last 5 datasets | Token |
| `GET` | `/api/history/<id>/` | Get dataset details | Token |
| `GET` | `/api/report/<id>/` | Download PDF report | Token |

### CSV Format

Required columns: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A,Vessel,120.5,5.2,110.0
Pump-Main,Pump,500.0,10.0,40.0
HeatEx-1,Heat Exchanger,250.0,3.5,85.0
```

---

## Sample Data

Use the included `sample_equipment_data.csv` with 16 equipment entries across 7 types:
- Vessels, Pumps, Heat Exchangers, Columns, Compressors, Mixers, Separators

---

## Configuration Notes

**Backend URL:** Both frontends connect to `http://127.0.0.1:8000`

**CORS Origins:** Pre-configured for `localhost:5173` and `localhost:3000`. Update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py` if needed.

---

## Usage Guide

1. **Start Backend** - Run Django server first
2. **Login** - Use created credentials in web or desktop app
3. **Upload** - Select the sample CSV or your own equipment data
4. **Analyze** - View auto-generated charts and statistics
5. **Export** - Download PDF report from History section

---

## Testing

```bash
cd backend
python manage.py test api.tests
```

---

## License

This project was developed as part of the FOSSEE Semester Internship 2026 screening task.
