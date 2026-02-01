# Testing Documentation

## How to Run Tests

```bash
cd backend
python manage.py test api.tests -v 2
```

## Expected Output

- 16+ tests passing
- CSV validation: 8 tests
- View logic: 8 tests (login, upload, history, compare, report)

## Test Categories

### 1. CSV Upload Validation
- ✅ Valid CSV with correct columns
- ✅ Reject non-CSV files
- ✅ Reject files >10MB
- ✅ Reject CSV with missing columns
- ✅ Reject CSV with invalid numeric values

### 2. Authentication
- ✅ Login with valid credentials
- ✅ Reject invalid credentials
- ✅ Token persists across sessions
- ✅ Logout clears token

### 3. Data Processing
- ✅ Correct average calculations
- ✅ Type distribution accurate
- ✅ History limited to 5 entries
- ✅ Oldest entries deleted

### 4. Dataset Comparison
- ✅ Compare requires authentication
- ✅ Rejects missing dataset IDs
- ✅ Returns 404 for missing datasets
- ✅ Returns comparison with diff values

### 5. PDF Generation
- ✅ Report contains all statistics
- ✅ Table formatted correctly
- ✅ Download triggers properly

### 6. Cross-Platform
- ✅ Web app works on Chrome/Firefox/Edge
- ✅ Desktop app runs on Windows/Linux

## Test Data

Using `sample_equipment_data.csv`:
- 15 rows
- 5 equipment types
- Expected averages:
  - Flowrate: ~184.37
  - Pressure: ~4.99
  - Temperature: ~68.33
