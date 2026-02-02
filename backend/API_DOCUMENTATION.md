# Backend API Documentation

This document outlines the REST API endpoints available in the Chemical Equipment Parameter Visualizer backend.

**Base URL:** `/api/`
**Authentication:** Token-based (Header: `Authorization: Token <key>`)

## Authentication

### 1. Login
- **Endpoint:** `/api/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and returns an auth token.
- **Request Body:**
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "user1"
  }
  ```

### 2. Register
- **Endpoint:** `/api/register/`
- **Method:** `POST`
- **Description:** Creates a new user account.
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "optional@example.com"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "token": "...",
    "user_id": 2,
    "username": "newuser"
  }
  ```

---

## Data Management

### 3. Upload Dataset
- **Endpoint:** `/api/upload/`
- **Method:** `POST`
- **Permissions:** IsAuthenticated
- **Rate Limit:** 10 requests / minute
- **Description:** Uploads a CSV file for analysis. The server parses the file, calculates statistics, and stores it.
- **Request Body:** `multipart/form-data`
  - `file`: (File, .csv)
- **Response (201 Created):**
  ```json
  {
    "id": 15,
    "filename": "equipment_data.csv",
    "uploaded_at": "2024-05-20T10:30:00Z",
    "total_count": 50,
    "avg_flowrate": 105.5,
    "avg_pressure": 12.3,
    "avg_temperature": 45.2,
    "type_distribution": {"Pump": 20, "Valve": 30}
  }
  ```

### 4. Get Upload History
- **Endpoint:** `/api/history/`
- **Method:** `GET`
- **Description:** Retrieves the last 5 uploaded datasets for the authenticated user.
- **Response (200 OK):** Array of dataset objects (same structure as Upload response).

### 5. Get Dataset Detail
- **Endpoint:** `/api/dataset/<id>/`
- **Method:** `GET`
- **Description:** Retrieves summary statistics for a specific dataset.
- **Response (200 OK):**
  ```json
  {
    "total_count": 50,
    "averages": {
      "flowrate": 105.5,
      "pressure": 12.3,
      "temperature": 45.2
    },
    "type_distribution": {"Pump": 20, "Valve": 30}
  }
  ```

### 6. Get Visualization Data
- **Endpoint:** `/api/visualize/<id>/`
- **Method:** `GET`
- **Description:** Returns formatted data for frontend charting (Chart.js / Recharts).
- **Response (200 OK):**
  ```json
  {
    "averages": { "labels": [...], "data": [...], "min": [...], "max": [...] },
    "type_distribution": { "labels": [...], "data": [...] }
  }
  ```

---

## Analytics & Reporting

### 7. Compare Datasets
- **Endpoint:** `/api/compare/`
- **Method:** `POST`
- **Description:** Compares two datasets and returns the difference in average parameters.
- **Request Body:**
  ```json
  {
    "dataset1": 15,
    "dataset2": 14
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "dataset1": { ... },
    "dataset2": { ... },
    "comparison": {
      "flowrate_diff": 5.2,
      "pressure_diff": -1.1,
      "temperature_diff": 0.5
    }
  }
  ```

### 8. Generate PDF Report
- **Endpoint:** `/api/report/<id>/`
- **Method:** `GET`
- **Description:** Generates and downloads a comprehensive PDF report for the dataset, including metadata, statistics tables, and charts.
- **Response:** Binary PDF file (`application/pdf`).
