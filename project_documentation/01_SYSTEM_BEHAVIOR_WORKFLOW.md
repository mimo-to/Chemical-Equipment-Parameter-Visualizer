# System Behavior and End-to-End Workflow

## Project Identity

**Title:** Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

**Scope:** Hybrid application running as both Web Application and Desktop Application for chemical equipment data visualization and analytics.

## System Architecture

Three-tier architecture with shared backend:

1. **Backend:** Django + Django REST Framework (single instance)
2. **Web Frontend:** React.js + Chart.js
3. **Desktop Frontend:** PyQt5 + Matplotlib

Both frontends are independent clients consuming the same backend API.

## Technology Stack (Fixed)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Browser-based tables and charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Desktop application tables and charts |
| Backend | Django + Django REST Framework | API server for both frontends |
| Data Processing | Pandas | CSV parsing and analytics |
| Database | SQLite | Persistent storage for last 5 datasets |
| Version Control | Git & GitHub | Source code management |

## End-to-End Workflow

### Workflow 1: CSV Upload and Analysis (Web)

1. User opens React web application in browser
2. User authenticates with credentials
3. User selects CSV file through file input
4. React sends POST request with CSV file to backend `/api/upload/`
5. Backend authenticates request
6. Backend parses CSV using Pandas
7. Backend validates required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
8. Backend computes analytics: total count, averages, type distribution
9. Backend stores dataset in SQLite (maintains last 5 only)
10. Backend returns JSON response with summary statistics and dataset ID
11. React receives response and displays summary data
12. React requests visualization data from backend
13. Backend returns data formatted for Chart.js
14. React renders charts using Chart.js

### Workflow 2: CSV Upload and Analysis (Desktop)

1. User launches PyQt5 desktop application
2. User authenticates with credentials
3. User selects CSV file through file dialog
4. PyQt5 sends POST request with CSV file to backend `/api/upload/`
5. Backend authenticates request
6. Backend parses CSV using Pandas
7. Backend validates required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
8. Backend computes analytics: total count, averages, type distribution
9. Backend stores dataset in SQLite (maintains last 5 only)
10. Backend returns JSON response with summary statistics and dataset ID
11. PyQt5 receives response and displays summary data
12. PyQt5 requests visualization data from backend
13. Backend returns data formatted for plotting
14. PyQt5 renders charts using Matplotlib

### Workflow 3: View History

1. User requests dataset history (web or desktop)
2. Frontend sends GET request to `/api/history/`
3. Backend retrieves last 5 datasets from SQLite ordered by upload time descending
4. Backend returns JSON array of datasets with summaries
5. Frontend displays history list with timestamps and statistics

### Workflow 4: Generate PDF Report

1. User requests PDF report for a specific dataset
2. Frontend sends GET request to `/api/report/<dataset_id>/`
3. Backend retrieves dataset from SQLite
4. Backend generates PDF with summary statistics
5. Backend returns PDF file as response
6. Frontend triggers download in browser or saves file in desktop app

### Workflow 5: Authentication

1. User provides username and password
2. Frontend sends credentials to authentication endpoint
3. Backend validates credentials
4. Backend returns authentication token
5. Frontend stores token
6. Frontend includes token in all subsequent API requests
7. Backend validates token on each protected endpoint

## Data Flow

### CSV File → Backend

- Transport: HTTP multipart/form-data
- Validation: File extension, required columns, numeric data types
- Processing: Pandas DataFrame parsing
- Expected Structure: 5 columns (Equipment Name, Type, Flowrate, Pressure, Temperature)
- Expected Data Types: String, String, Numeric, Numeric, Numeric
- Dataset Size: Arbitrary number of rows (sample contains 15 rows for demo)

### Backend → Frontend (Summary)

- Transport: HTTP JSON response
- Content: Total count, averages, type distribution, dataset ID, timestamp

### Backend → Frontend (Visualization Data)

- Transport: HTTP JSON response
- Content: Arrays of values for chart rendering

### Backend → Database

- Storage: SQLite database with EquipmentDataset model
- Constraint: Maximum 5 datasets retained

## Application States

### Web Application States

1. **Unauthenticated:** Login form visible, API access blocked
2. **Authenticated - Idle:** Upload button enabled, no data displayed
3. **Uploading:** File selected, upload in progress, loading indicator
4. **Data Loaded:** Summary statistics visible, charts rendered
5. **Viewing History:** List of past 5 uploads displayed
6. **Generating Report:** PDF generation in progress

### Desktop Application States

1. **Unauthenticated:** Login dialog visible, main window disabled
2. **Authenticated - Idle:** File selection enabled, no data displayed
3. **Uploading:** File selected, upload in progress, progress indicator
4. **Data Loaded:** Summary statistics visible, charts rendered
5. **Viewing History:** History window or panel showing past 5 uploads
6. **Generating Report:** PDF save dialog after generation

## Error Handling Behavior

### CSV Upload Errors

- **Missing columns:** Return 400 error with message specifying missing columns
- **Invalid data types:** Return 400 error with row number and column name
- **Empty file:** Return 400 error indicating file is empty
- **File too large:** Return 413 error if file exceeds size limit

### Authentication Errors

- **Invalid credentials:** Return 401 error
- **Missing token:** Return 401 error
- **Expired token:** Return 401 error requiring re-authentication

### Database Errors

- **Storage failure:** Return 500 error, log error details
- **Query failure:** Return 500 error, log error details

## Concurrent Access Behavior

- Backend handles multiple simultaneous uploads from different users
- Each upload is independent transaction
- History management per upload maintains last 5 constraint atomically
- No shared state between web and desktop clients except through backend API

## Success Criteria

A complete implementation must:

1. Allow CSV upload from both web and desktop clients
2. Parse CSV and compute required analytics correctly
3. Store exactly last 5 datasets in database
4. Display data tables and charts in both frontends
5. Generate downloadable PDF reports
6. Enforce authentication on all protected endpoints
7. Handle errors gracefully with appropriate HTTP status codes
8. Maintain data consistency across multiple uploads
