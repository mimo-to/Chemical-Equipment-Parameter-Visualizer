# Web Frontend Interaction Rules (React)

## Technology Stack

**Framework:** React.js

**Charting Library:** Chart.js

**HTTP Client:** fetch API or axios

**Build Tool:** Create React App or Vite (either acceptable)

## Application Structure

### Component Organization

```
src/
├── App.js
├── components/
│   ├── Login.js
│   ├── Upload.js
│   ├── DataTable.js
│   ├── Charts.js
│   └── History.js
├── services/
│   └── api.js
└── index.js
```

**App.js:** Main application component, routing, authentication state

**Login.js:** Login form and authentication logic

**Upload.js:** CSV file upload interface

**DataTable.js:** Display equipment data in table format

**Charts.js:** Render charts using Chart.js

**History.js:** Display list of past 5 datasets

**api.js:** Centralized API calls to backend

## Authentication Flow

### Initial State

**User Not Authenticated:**

- Display login form
- Hide main application content
- Store no token

### Login Process

**Step 1:** User enters username and password in login form

**Step 2:** Form submission triggers POST to `/api/login/`

```javascript
const response = await fetch('http://localhost:8000/api/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
});
```

**Step 3:** If response status is 200:

- Extract token from response JSON
- Store token in localStorage or sessionStorage
- Update application state to authenticated
- Display main application interface

**Step 4:** If response status is 401 or 400:

- Display error message to user
- Keep login form visible
- Do not store token

### Token Storage

**Method:** localStorage or sessionStorage

**Key:** `authToken`

**Storage:**

```javascript
localStorage.setItem('authToken', token);
```

**Retrieval:**

```javascript
const token = localStorage.getItem('authToken');
```

### Authenticated Requests

All API requests except login must include Authorization header:

```javascript
const response = await fetch(url, {
    headers: {
        'Authorization': `Token ${token}`
    }
});
```

### Session Persistence

**On Page Load:**

- Check if token exists in localStorage
- If exists, assume authenticated and proceed to main interface
- If not exists, show login form

**Logout (Optional):**

- Clear token from localStorage
- Reset application state to unauthenticated
- Redirect to login form

### Handling 401 Responses

**On Any 401 Error:**

- Clear token from storage
- Update state to unauthenticated
- Redirect to login form
- Display message: "Session expired, please login again"

## CSV Upload Interface

### Upload Component

**Elements:**

- File input field (accept=".csv")
- Upload button
- Status indicator (loading, success, error)
- Display area for results

### Upload Process

**Step 1:** User selects CSV file using file input

**Step 2:** File is stored in component state

**Step 3:** User clicks upload button

**Step 4:** Create FormData and append file

```javascript
const formData = new FormData();
formData.append('file', file);
```

**Step 5:** Send POST request to `/api/upload/`

```javascript
const response = await fetch('http://localhost:8000/api/upload/', {
    method: 'POST',
    headers: {
        'Authorization': `Token ${token}`
    },
    body: formData
});
```

**Step 6:** Handle response

- If 201: Parse JSON, store dataset summary, display success
- If 400: Parse error message, display to user
- If 401: Redirect to login
- If 413: Display "File too large" error

### Upload Feedback

**During Upload:**

- Disable upload button
- Show loading spinner or progress indicator
- Display "Uploading..." message

**On Success:**

- Display summary statistics
- Request and render charts
- Refresh history list
- Re-enable upload for new file

**On Error:**

- Display error message from backend
- Re-enable upload button
- Keep file input available

## Data Display

### Summary Statistics Table

**Content:** Display values from upload response

**Format:** Table or list

**Fields:**

- Filename
- Upload timestamp (formatted)
- Total count
- Average flowrate
- Average pressure
- Average temperature

**Formatting:**

- Timestamps: Human-readable format (e.g., "Jan 28, 2026 2:30 PM")
- Numbers: 2 decimal places for averages

### Equipment Data Table (Optional)

**Not Required by Specification**

**If Implemented:** Display individual equipment rows from CSV

**Note:** Backend does not provide raw CSV data in response, only summaries

## Chart Visualization

### Chart Library Integration

**Import Chart.js:**

```javascript
import { Chart } from 'chart.js/auto';
```

Or use React wrapper:

```javascript
import { Bar, Pie } from 'react-chartjs-2';
```

### Required Charts

**Chart 1: Type Distribution**

**Type:** Bar chart or Pie chart

**Data Source:** `type_distribution` from upload response or visualization endpoint

**X-Axis (Bar):** Equipment types

**Y-Axis (Bar):** Count

**Segments (Pie):** Equipment types with count as value

**Chart 2: Average Values**

**Type:** Bar chart

**Data Source:** Average flowrate, pressure, temperature

**X-Axis:** Parameter names (Flowrate, Pressure, Temperature)

**Y-Axis:** Average values

### Visualization Data Retrieval

**Option 1:** Use data from upload response

**Option 2:** Call `/api/dataset/<id>/visualization/` endpoint

```javascript
const response = await fetch(`http://localhost:8000/api/dataset/${datasetId}/visualization/`, {
    headers: {
        'Authorization': `Token ${token}`
    }
});
const vizData = await response.json();
```

**Response Format (example based on sample dataset):**

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

Note: Type labels and data arrays are fully data-driven. Different datasets will have different labels and counts.

### Chart Rendering

**Type Distribution Chart:**

```javascript
const typeChartData = {
    labels: vizData.type_distribution.labels,
    datasets: [{
        label: 'Equipment Count by Type',
        data: vizData.type_distribution.data,
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
};
```

Note: Sample dataset demonstrates equal distribution (5 each), but charts must render any distribution dynamically. Type labels and counts vary by dataset.

**Averages Chart:**

```javascript
const avgChartData = {
    labels: vizData.averages.labels,
    datasets: [{
        label: 'Average Values',
        data: vizData.averages.data,
        backgroundColor: '#4BC0C0'
    }]
};
```

Note: Average values shown are illustrative based on sample. Actual values computed from uploaded data.

### Chart Display

**Container:** Dedicated div or section for each chart

**Responsive:** Charts should resize with viewport

**Legend:** Include legend for clarity

**Labels:** Clear axis labels and titles

## History Display

### History Component

**Purpose:** Display list of last 5 uploaded datasets

**Data Source:** GET `/api/history/`

**Trigger:** Load on component mount, refresh after each upload

### History Retrieval

```javascript
const response = await fetch('http://localhost:8000/api/history/', {
    headers: {
        'Authorization': `Token ${token}`
    }
});
const history = await response.json();
```

### History List Display

**Format:** Table or list of dataset cards

**Columns/Fields:**

- Dataset ID
- Filename
- Upload timestamp
- Total count
- Type distribution summary

**Interaction:** Click on item to view details or generate report

**Ordering:** Most recent first (backend provides correct order)

### Empty History

**Condition:** No datasets uploaded yet

**Display:** Message "No datasets uploaded yet" or empty state illustration

## PDF Report Generation

### Trigger

**User Action:** Click "Generate Report" button for a dataset

**Location:** History list or dataset details view

### Report Request

```javascript
const response = await fetch(`http://localhost:8000/api/report/${datasetId}/`, {
    headers: {
        'Authorization': `Token ${token}`
    }
});
```

### Download Handling

**Step 1:** Convert response to blob

```javascript
const blob = await response.blob();
```

**Step 2:** Create object URL

```javascript
const url = window.URL.createObjectURL(blob);
```

**Step 3:** Create download link and trigger click

```javascript
const a = document.createElement('a');
a.href = url;
a.download = `report_${datasetId}.pdf`;
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
window.URL.revokeObjectURL(url);
```

### Report Generation Feedback

**During Generation:**

- Show loading indicator
- Disable button
- Display "Generating report..." message

**On Success:**

- Trigger download automatically
- Show success message
- Re-enable button

**On Error:**

- Display error message
- Re-enable button

## Error Handling

### Network Errors

**Scenario:** Backend not reachable

**Handling:**

- Catch fetch errors
- Display user-friendly message: "Cannot connect to server"
- Provide retry option

### Validation Errors (400)

**Scenario:** CSV validation failed

**Handling:**

- Parse error message from response
- Display specific error to user
- Example: "Missing required columns: Pressure"

### Authentication Errors (401)

**Scenario:** Token invalid or expired

**Handling:**

- Clear stored token
- Redirect to login
- Display: "Session expired, please login again"

### Not Found Errors (404)

**Scenario:** Dataset does not exist (deleted from history)

**Handling:**

- Display: "Dataset not found (may have been removed)"
- Refresh history list
- Remove stale dataset from UI

### Server Errors (500)

**Scenario:** Backend processing error

**Handling:**

- Display: "Server error, please try again"
- Log error to console for debugging

## State Management

### Application State

**Recommended:** React useState or useContext for simple state

**Optional:** Redux or other state management library (not required for this scope)

### State Variables

**authToken:** String or null

**isAuthenticated:** Boolean

**currentDataset:** Object or null (currently displayed dataset)

**history:** Array of dataset objects

**uploadStatus:** String (idle, uploading, success, error)

**errorMessage:** String or null

### State Updates

**On Login Success:** Set authToken, isAuthenticated = true

**On Upload Success:** Set currentDataset, refresh history

**On Logout:** Clear authToken, isAuthenticated = false, reset other state

## Routing (Optional)

**Not Required:** Single-page application without routing is acceptable

**If Implemented:** Use React Router

**Routes:**

- `/` - Login or main dashboard
- `/upload` - Upload interface
- `/history` - History view
- `/dataset/:id` - Dataset details

## UI/UX Requirements

### Responsive Design

**Not Strictly Required:** Desktop-focused is acceptable

**Recommended:** Basic responsive layout for different screen sizes

### Styling

**Method:** CSS, CSS modules, or styled-components

**Framework:** Bootstrap, Material-UI, Tailwind (optional, not required)

**Minimum:** Clean, readable interface with proper spacing

### User Feedback

**Loading States:** Show spinners or progress indicators during async operations

**Success Messages:** Confirm successful actions (upload, login)

**Error Messages:** Clear, actionable error descriptions

**Disabled States:** Disable buttons during processing to prevent double-submission

## Browser Compatibility

**Target:** Modern browsers (Chrome, Firefox, Safari, Edge)

**ES6+:** Use modern JavaScript features (supported by Create React App)

**Fetch API:** Native browser API, no polyfill needed for modern browsers

## Development Server

**Command:** `npm start` or `yarn start`

**Port:** Default 3000 (configurable)

**Hot Reload:** Automatic reload on code changes

**Proxy:** Configure proxy to backend if needed to avoid CORS issues

## Build and Deployment

**Build Command:** `npm run build` or `yarn build`

**Output:** Optimized static files in `build/` directory

**Deployment:** Can deploy to any static hosting (Netlify, Vercel, GitHub Pages)

**Optional:** Task specifies "Optional: Deployment link for web version"

## Sample Data Handling

**File:** `sample_equipment_data.csv`

**Purpose:** Demo validation and testing reference

**Structure:** 15 rows, 5 columns (example size; system handles arbitrary row counts)

**Column Schema:**
- Equipment Name (String)
- Type (String) - Sample contains: Reactor, Heat Exchanger, Pump
- Flowrate (Numeric) - Sample contains integer values
- Pressure (Numeric) - Sample contains float values
- Temperature (Numeric) - Sample contains integer values

**Usage:** Demonstrate upload functionality and verify analytics computation

**Location:** Include in repository root directory

**Testing:** Use this file to verify CSV parsing, analytics, charts, and PDF generation. System must handle any valid CSV following the same schema with different data values, row counts, and type distributions.
