# API Documentation

## Base URL
Local: `http://127.0.0.1:8000/api`
Production: `https://<your-render-app>.onrender.com/api`

---

## 🟢 System Health

### Check System Status
**GET /health/**  
**HEAD /health/**
*   **Auth Required**: No
*   **Description**: Used by frontend for "Server Warming" ping to wake up free-tier instances.
*   **Response (200 OK)**:
    ```json
    { "status": "ok" }
    ```

---

## 🔐 Authentication

### Register New User
**POST /register/**
*   **Auth Required**: No
*   **Body**:
    ```json
    {
        "username": "engineer1",
        "password": "securepassword123",
        "email": "engineer@example.com"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
        "token": "<your_generated_token>",
        "user_id": 1,
        "username": "engineer1"
    }
    ```

### Login
**POST /login/**
*   **Auth Required**: No
*   **Body**:
    ```json
    {
        "username": "engineer1",
        "password": "securepassword123"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
        "token": "<your_generated_token>",
        "user_id": 1,
        "username": "engineer1"
    }
    ```

---

## 📂 Data Management

### Upload Dataset
**POST /upload/**
*   **Auth Required**: Yes (`Authorization: Token <key>`)
*   **Rate Limit**: 10 requests per minute per user.
*   **Body**: `Multipart/Form-Data`
    *   `file`: (Binary CSV file)
*   **CSV Requirements**:
    *   Max Size: 10MB
    *   Required Columns: `Equipment Name`, `Timestamp`, `Flowrate`, `Pressure`, `Temperature`, `Type`
*   **Response (201 Created)**:
    ```json
    {
        "id": 15,
        "filename": "batch_process_data.csv",
        "total_count": 100,
        "avg_flowrate": 45.2,
        ...
    }
    ```
*   **Errors**:
    *   `400 Bad Request`: Invalid CSV structure, missing columns, or non-numeric data.

### Get Upload History
**GET /history/**
*   **Auth Required**: Yes
*   **Description**: Retrieves the last 5 uploads for the authenticated user.
*   **Response (200 OK)**: Array of Dataset objects.

### Get Dataset Detail
**GET /dataset/<id>/**
*   **Auth Required**: Yes
*   **Response (200 OK)**:
    ```json
    {
        "total_count": 100,
        "averages": { "flowrate": 45.2, ... },
        "type_distribution": { "Pump": 12, "Valve": 8 }
    }
    ```

---

## 📊 Analysis & Reporting

### Get Visualization Data
**GET /dataset/<id>/visualization/**
*   **Auth Required**: Yes
*   **Description**: Returns formatted data for specific frontend charts.
*   **Response (200 OK)**:
    ```json
    {
        "type_distribution": { "labels": ["Pump", "Tank"], "data": [10, 5] },
        "averages": { "labels": ["Flowrate", ...], "data": [45.2, ...], "min": [...], "max": [...] }
    }
    ```

### Compare Datasets
**POST /compare/**
*   **Auth Required**: Yes
*   **Body**:
    ```json
    {
        "dataset1": 15,
        "dataset2": 14
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
        "dataset1": { ... },
        "dataset2": { ... },
        "comparison": {
            "flowrate_diff": 1.5,
            "pressure_diff": -0.2,
            ...
        }
    }
    ```

### Download PDF Report
**GET /report/<id>/**
*   **Auth Required**: Yes
*   **Response (200 OK)**: Binary Blob (`application/pdf`)
