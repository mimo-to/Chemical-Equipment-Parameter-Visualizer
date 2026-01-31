# API Contracts and Endpoints

## Base URL

**Development:** `http://localhost:8000`

**API Prefix:** `/api/`

## Authentication

All endpoints except `/api/login/` require authentication.

**Authentication Method:** Token-based

**Header Format:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Endpoint 1: User Login

### POST /api/login/

**Purpose:** Authenticate user and receive access token

**Authentication Required:** No

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
    "username": "testuser",
    "password": "testpassword"
}
```

**Success Response:**

**Status Code:** 200 OK

**Response Body:**

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "testuser"
}
```

**Error Responses:**

**Status Code:** 400 Bad Request

**Response Body:**

```json
{
    "error": "Username and password required"
}
```

**Status Code:** 401 Unauthorized

**Response Body:**

```json
{
    "error": "Invalid credentials"
}
```

## Endpoint 2: Upload CSV

### POST /api/upload/

**Purpose:** Upload CSV file, parse data, compute analytics, store dataset

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Token <token>
Content-Type: multipart/form-data
```

**Request Body:**

Multipart form data with field:

- `file`: CSV file upload

**Success Response:**

**Status Code:** 201 Created

**Response Body (example based on sample dataset):**

```json
{
    "id": 1,
    "filename": "sample_equipment_data.csv",
    "uploaded_at": "2026-01-28T10:30:00.123Z",
    "total_count": 15,
    "avg_flowrate": 112.53,
    "avg_pressure": 14.37,
    "avg_temperature": 316.87,
    "type_distribution": {
        "Reactor": 5,
        "Heat Exchanger": 5,
        "Pump": 5
    }
}
```

**Note:** Values shown are illustrative. Actual total_count, averages, and type_distribution depend entirely on uploaded CSV content.

**Response Fields:**

- `id`: Integer, unique dataset identifier
- `filename`: String, original filename
- `uploaded_at`: ISO 8601 datetime string in UTC
- `total_count`: Integer, number of equipment rows
- `avg_flowrate`: Float, rounded to 2 decimal places
- `avg_pressure`: Float, rounded to 2 decimal places
- `avg_temperature`: Float, rounded to 2 decimal places
- `type_distribution`: Object, equipment types mapped to counts

**Error Responses:**

**Status Code:** 400 Bad Request (No file provided)

```json
{
    "error": "No file provided"
}
```

**Status Code:** 400 Bad Request (Invalid file type)

```json
{
    "error": "File must be a CSV"
}
```

**Status Code:** 400 Bad Request (Missing columns)

```json
{
    "error": "Missing required columns: Flowrate, Pressure"
}
```

**Status Code:** 400 Bad Request (Invalid data)

```json
{
    "error": "Invalid numeric value in row 3, column Flowrate"
}
```

**Status Code:** 400 Bad Request (Empty file)

```json
{
    "error": "CSV file is empty"
}
```

**Status Code:** 401 Unauthorized (Missing or invalid token)

```json
{
    "error": "Authentication credentials were not provided"
}
```

**Status Code:** 413 Payload Too Large (File size exceeds limit)

```json
{
    "error": "File size exceeds 10MB limit"
}
```

## Endpoint 3: Get Dataset History

### GET /api/history/

**Purpose:** Retrieve list of last 5 uploaded datasets with summaries

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Token <token>
```

**Request Body:** None

**Success Response:**

**Status Code:** 200 OK

**Response Body:**

```json
[
    {
        "id": 5,
        "filename": "data5.csv",
        "uploaded_at": "2026-01-28T14:00:00.000Z",
        "total_count": 8,
        "avg_flowrate": 120.0,
        "avg_pressure": 16.0,
        "avg_temperature": 320.0,
        "type_distribution": {
            "Reactor": 5,
            "Pump": 3
        }
    },
    {
        "id": 4,
        "filename": "data4.csv",
        "uploaded_at": "2026-01-28T13:00:00.000Z",
        "total_count": 10,
        "avg_flowrate": 110.0,
        "avg_pressure": 14.0,
        "avg_temperature": 300.0,
        "type_distribution": {
            "Reactor": 6,
            "Heat Exchanger": 4
        }
    },
    {
        "id": 3,
        "filename": "data3.csv",
        "uploaded_at": "2026-01-28T12:00:00.000Z",
        "total_count": 12,
        "avg_flowrate": 105.5,
        "avg_pressure": 13.5,
        "avg_temperature": 295.0,
        "type_distribution": {
            "Reactor": 7,
            "Heat Exchanger": 5
        }
    }
]
```

**Response Ordering:** Most recent upload first (descending by `uploaded_at`)

**Response Limit:** Maximum 5 datasets

**Empty Response:**

```json
[]
```

**Error Responses:**

**Status Code:** 401 Unauthorized

```json
{
    "error": "Authentication credentials were not provided"
}
```

## Endpoint 4: Get Dataset Details

### GET /api/dataset/<int:id>/

**Purpose:** Retrieve full details of a specific dataset

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Token <token>
```

**URL Parameters:**

- `id`: Integer, dataset identifier

**Request Body:** None

**Success Response:**

**Status Code:** 200 OK

**Response Body:**

```json
{
    "id": 1,
    "filename": "sample_equipment_data.csv",
    "uploaded_at": "2026-01-28T10:30:00.123Z",
    "total_count": 10,
    "avg_flowrate": 115.56,
    "avg_pressure": 15.23,
    "avg_temperature": 310.45,
    "type_distribution": {
        "Reactor": 4,
        "Heat Exchanger": 3,
        "Pump": 3
    }
}
```

**Error Responses:**

**Status Code:** 401 Unauthorized

```json
{
    "error": "Authentication credentials were not provided"
}
```

**Status Code:** 404 Not Found

```json
{
    "error": "Dataset not found"
}
```

## Endpoint 5: Get Visualization Data

### GET /api/dataset/<int:id>/visualization/

**Purpose:** Retrieve data formatted for chart rendering

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Token <token>
```

**URL Parameters:**

- `id`: Integer, dataset identifier

**Request Body:** None

**Success Response:**

**Status Code:** 200 OK

**Response Body (example based on sample dataset):**

```json
{
    "type_distribution": {
        "labels": ["Reactor", "Heat Exchanger", "Pump"],
        "data": [5, 5, 5]
    },
    "averages": {
        "labels": ["Flowrate", "Pressure", "Temperature"],
        "data": [112.53, 14.37, 316.87]
    }
}
```

**Note:** Values shown are illustrative. Labels and counts in type_distribution are data-driven and vary by dataset.

**Response Structure:**

- `type_distribution.labels`: Array of equipment type names
- `type_distribution.data`: Array of counts corresponding to labels
- `averages.labels`: Array of parameter names
- `averages.data`: Array of average values corresponding to labels

**Error Responses:**

**Status Code:** 401 Unauthorized

```json
{
    "error": "Authentication credentials were not provided"
}
```

**Status Code:** 404 Not Found

```json
{
    "error": "Dataset not found"
}
```

## Endpoint 6: Generate PDF Report

### GET /api/report/<int:id>/

**Purpose:** Generate and download PDF report for dataset

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Token <token>
```

**URL Parameters:**

- `id`: Integer, dataset identifier

**Request Body:** None

**Success Response:**

**Status Code:** 200 OK

**Response Headers:**

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="report_<dataset_id>.pdf"
```

**Response Body:** Binary PDF file content

**Error Responses:**

**Status Code:** 401 Unauthorized

```json
{
    "error": "Authentication credentials were not provided"
}
```

**Status Code:** 404 Not Found

```json
{
    "error": "Dataset not found"
}
```

**Status Code:** 500 Internal Server Error

```json
{
    "error": "Failed to generate PDF report"
}
```

## CORS Configuration

**Required for Web Frontend:** Enable CORS to allow React app on different port/domain

**Allowed Origins:** Configure based on deployment

**Development:** `http://localhost:3000`

**Allowed Methods:** GET, POST, OPTIONS

**Allowed Headers:** Authorization, Content-Type

## Rate Limiting

**Not Required:** Task specification does not mandate rate limiting

**Optional:** May implement if desired for production readiness

## Pagination

**Not Required:** History endpoint returns maximum 5 items, no pagination needed

## Data Format Standards

[Clarification Added: API response consistency explanation]

**Response Format Consistency:** All endpoints use JSON responses. Error responses consistently use `{"error": "message"}` format across all endpoints. Success response structures vary intentionally by endpoint purpose (e.g., dataset objects, arrays, PDF binary content) but maintain consistent field naming and data type conventions.

### DateTime Format

**Standard:** ISO 8601 with UTC timezone

**Example:** `2026-01-28T10:30:00.123Z`

### Numeric Precision

**Averages:** Round to 2 decimal places

**Counts:** Integer values only

### Boolean Values

**Format:** `true` or `false` (lowercase)

### Null Values

**Representation:** `null`

**Usage:** Not expected in required fields

## HTTP Status Code Usage

### Success Codes

- **200 OK:** Successful GET requests
- **201 Created:** Successful POST for new resource creation

### Client Error Codes

- **400 Bad Request:** Invalid request data, validation errors
- **401 Unauthorized:** Authentication failed or missing
- **404 Not Found:** Resource does not exist
- **413 Payload Too Large:** File size exceeds limit

### Server Error Codes

- **500 Internal Server Error:** Unexpected server-side failure

## Request Size Limits

**CSV File Upload:** Maximum 10MB

**JSON Request Body:** Maximum 1MB

## Response Time Expectations

**Upload Endpoint:** May take several seconds for large CSV files

**Other Endpoints:** Should respond within 1 second

**PDF Generation:** May take several seconds depending on dataset size
