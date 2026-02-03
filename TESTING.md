# 🧪 Testing & Validation Guide

This document outlines the validation protocols used to ensure the reliability and correctness of the Chemical Equipment Parameter Visualizer.

---

## 1. Automated Backend Tests

The Django backend includes a suite of tests to verify core logic, authentication, and data processing.

### Running the Test Suite
To execute all automated tests, run the following command from the `backend/` directory:

```bash
python manage.py test
```

### Coverage Areas
1.  **Authentication**:
    *   Verifies user registration and token generation.
    *   Ensures protected endpoints (`/upload/`, `/history/`) reject unauthenticated requests (401 Unauthorized).
2.  **CSV Schema Validation**:
    *   **Valid Uploads**: Confirms that correctly formatted CSVs are processed and stored.
    *   **Invalid Uploads**: Checks that files missing required columns (`Flowrate`, `Pressure`) are rejected with `400 Bad Request`.
    *   **Data Types**: Ensures non-numeric values in numeric columns trigger validation errors.
3.  **Analytics Engine**:
    *   Verifies that `Pandas` correctly calculates `mean`, `min`, and `max` for uploaded datasets.
    *   Compares output against known deterministic values.

---

## 2. Manual End-to-End Verification

Evaluators can perform the following manual checks to validate the full system flow.

### Phase 1: Ingestion & Analysis
1.  **Login**: Use the Web Client or Desktop App to log in.
2.  **Upload**: Drag & Drop the provided `sample_equipment_data.csv`.
3.  **Verify**:
    *   A "Success" toast appears.
    *   The "Analysis Results" dashboard automatically populates with Charts and Summary Statistics.

### Phase 2: Cross-Client Consistency
1.  **Web**: Upload a file via the React Web App.
2.  **Desktop**: Open the PyQt5 Desktop App and navigate to "History".
3.  **Verify**: The file uploaded via Web is immediately visible in the Desktop App, confirming the unified backend state.

### Phase 3: PDF Reporting
1.  **Action**: Click "Download Report" (Web) or "Export PDF" (Desktop).
2.  **Verify**:
    *   A PDF file is downloaded.
    *   Open the PDF: It should contain a vector-graphic Title, Summary Table, and visual Charts (Pie/Bar).

---

## 3. Deployment Validation (Render)

### Cold Start Test
1.  Navigate to the live deployment after >15 minutes of inactivity.
2.  Attempt to Login.
3.  **Observation**: The initial request may hang for ~50 seconds (Render Free Tier waking up).
4.  **Result**: Subsequent requests should be instant (<500ms).

### Data Persistence Test (Ephemeral)
1.  Upload a file.
2.  Wait for a manual redeploy or restart on the Render dashboard.
3.  **Observation**: The data disappears.
4.  **Confirmation**: This confirms the "Ephemeral Filesystem" constraint documented in the README.
