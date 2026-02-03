# API Documentation

This documentation details the RESTful endpoints provided by the Django backend.

## Base URL
*   **Local**: `http://127.0.0.1:8000/api`
*   **Production**: `https://<your-render-app>.onrender.com/api`

---

## 1. Upload Dataset

**POST** `/upload/`

Uploads a CSV file for analysis. Triggers validation and automatic statistical computation.

*   **Auth Required**: Yes (`Authorization: Token <token>`)
*   **Content-Type**: `multipart/form-data`

### Sample Request
```http
POST /api/upload/ HTTP/1.1
Authorization: Token <your_token>
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="equipment_data.csv"
Content-Type: text/csv

(CSV Content Here)
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

### Success Response (201 Created)
```json
{
  "id": 15,
  "filename": "equipment_data.csv",
  "total_count": 100,
  "uploaded_at": "2026-02-03T12:00:00Z",
  "averages": {
    "Flowrate": 45.2,
    "Pressure": 101.3,
    "Temperature": 25.4
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Missing required column: Flowrate"
}
```

---

## 2. Get Upload History

**GET** `/history/`

Retrieves the authenticated user's last 5 datasets.

*   **Auth Required**: Yes
*   **Content-Type**: `application/json`

### Sample Request
```http
GET /api/history/ HTTP/1.1
Authorization: Token <your_token>
```

### Success Response (200 OK)
```json
[
  {
    "id": 15,
    "filename": "batch_A.csv",
    "uploaded_at": "..."
  },
  {
    "id": 14,
    "filename": "batch_B.csv",
    "uploaded_at": "..."
  }
]
```

---

## 3. Get Dataset Detail

**GET** `/dataset/<id>/`

Retrieves detailed statistics for a specific dataset.

*   **Auth Required**: Yes
*   **Content-Type**: `application/json`

### Sample Request
```http
GET /api/dataset/15/ HTTP/1.1
Authorization: Token <your_token>
```

### Success Response (200 OK)
```json
{
  "id": 15,
  "total_count": 100,
  "averages": { "Flowrate": 45.2, "Pressure": 101.3 },
  "type_distribution": { "Pump": 12, "Valve": 8 }
}
```

---

## 4. Get Visualization Data

**GET** `/dataset/<id>/visualization/`

Returns formatted data specifically for frontend Chart.js rendering.

*   **Auth Required**: Yes
*   **Content-Type**: `application/json`

### Sample Request
```http
GET /api/dataset/15/visualization/ HTTP/1.1
Authorization: Token <your_token>
```

### Success Response (200 OK)
```json
{
  "type_distribution": {
    "labels": ["Pump", "Tank"],
    "data": [10, 5]
  },
  "averages": {
    "labels": ["Flowrate", "Pressure"],
    "data": [45.2, 101.3]
  }
}
```

---

## 5. Compare Datasets

**POST** `/compare/`

Compares two datasets side-by-side.

*   **Auth Required**: Yes
*   **Content-Type**: `application/json`

### Sample Request
```json
{
  "dataset1": 15,
  "dataset2": 14
}
```

### Success Response (200 OK)
```json
{
  "dataset1": { "filename": "batch_A.csv", "averages": { "Flowrate": 45 } },
  "dataset2": { "filename": "batch_B.csv", "averages": { "Flowrate": 40 } },
  "comparison": {
    "Flowrate_diff": 5,
    "Pressure_diff": 0
  }
}
```

---

## 6. Download PDF Report

**GET** `/report/<id>/`

Generates a vector-graphic PDF report.

*   **Auth Required**: Yes
*   **Response**: Binary Blob (`application/pdf`)

---

## 7. Authentication

### Register
**POST** `/register/`

### Sample Request
```json
{
  "username": "engineer1",
  "password": "securepassword123",
  "email": "engineer@example.com"
}
```

### Success Response (201 Created)
```json
{
  "token": "<your_generated_token>",
  "user_id": 1,
  "username": "engineer1"
}
```

### Login
**POST** `/login/`

### Sample Request
```json
{
  "username": "engineer1",
  "password": "securepassword123"
}
```

### Success Response (200 OK)
```json
{
  "token": "<your_generated_token>",
  "user_id": 1,
  "username": "engineer1"
}
```

---

## 8. System Health

**GET/HEAD** `/health/`

Used for "Server Warming" to mitigate Render Free Tier cold starts.

*   **Auth Required**: No
*   **Response**: `{"status": "ok"}`
