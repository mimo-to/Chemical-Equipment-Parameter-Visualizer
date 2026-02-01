# Testing Documentation

## Test Cases

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

### 4. PDF Generation
- ✅ Report contains all statistics
- ✅ Table formatted correctly
- ✅ Download triggers properly

### 5. Cross-Platform
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
