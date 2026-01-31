# Backend Responsibilities and Data Processing

## Backend Role

The Django backend is the single authoritative source for:

- CSV file reception and validation
- Data parsing and transformation
- Analytics computation
- Dataset storage and retrieval
- History management (last 5 constraint)
- PDF report generation
- Authentication and authorization
- API response formatting

## Project Structure

```
backend/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── utils.py
```

## Database Model

### EquipmentDataset Model

**File:** `api/models.py`

**Fields:**

- `id`: Integer, auto-increment primary key
- `uploaded_at`: DateTime, automatically set on creation
- `filename`: String (max 255 characters), original CSV filename
- `total_count`: Integer, total number of equipment rows
- `avg_flowrate`: Float, average flowrate value
- `avg_pressure`: Float, average pressure value
- `avg_temperature`: Float, average temperature value
- `type_distribution`: JSON, dictionary mapping equipment type to count
- `csv_data`: Text, complete CSV file content as string

**Indexes:**

- Primary key on `id`
- Index on `uploaded_at` for efficient ordering

**Constraints:**

- All numeric fields must accept null=False
- `uploaded_at` must have auto_now_add=True
- `type_distribution` stores JSON as: `{"Type1": count1, "Type2": count2, ...}`

## CSV Processing Logic

### File Reception

**Input:** HTTP multipart/form-data request with file field named `file`

**Validation Steps:**

1. Check file exists in request
2. Check file extension is `.csv`
3. Check file size is less than 10MB
4. Read file content into memory

**Error Response:** 400 Bad Request if any validation fails

### CSV Parsing

**Tool:** Pandas `read_csv()`

**Process:**

1. Read CSV content into Pandas DataFrame
2. Validate required columns present: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`
3. Check column names match exactly (case-sensitive)
4. Verify DataFrame is not empty

**Required Columns (Exact Names):**

- `Equipment Name`
- `Type`
- `Flowrate`
- `Pressure`
- `Temperature`

**Error Response:** 400 Bad Request with message listing missing columns

### Data Type Validation

**Numeric Columns:** `Flowrate`, `Pressure`, `Temperature`

**Validation:**

1. Attempt to convert to float using `pd.to_numeric()`
2. Check for NaN values after conversion
3. If NaN found, identify row numbers and column names

**Parsing Behavior:**
- All numeric columns are converted to float internally regardless of input format
- Integer values in CSV are acceptable and will be converted to float
- Decimal values are acceptable and converted to float
- Sample dataset contains mix of integer and float representations

**Error Response:** 400 Bad Request with message specifying row and column with invalid data

### Data Cleaning

**Steps:**

1. Strip whitespace from `Equipment Name` and `Type` columns
2. Convert `Flowrate`, `Pressure`, `Temperature` to float
3. Remove rows with any null values
4. Reset DataFrame index

**Result:** Clean DataFrame ready for analytics

## Analytics Computation

### Total Count

**Computation:** Number of rows in cleaned DataFrame

```python
total_count = len(df)
```

### Average Flowrate

**Computation:** Mean of `Flowrate` column

```python
avg_flowrate = df['Flowrate'].mean()
```

**Rounding:** Round to 2 decimal places

### Average Pressure

**Computation:** Mean of `Pressure` column

```python
avg_pressure = df['Pressure'].mean()
```

**Rounding:** Round to 2 decimal places

### Average Temperature

**Computation:** Mean of `Temperature` column

```python
avg_temperature = df['Temperature'].mean()
```

**Rounding:** Round to 2 decimal places

### Type Distribution

**Computation:** Count of each unique value in `Type` column

```python
type_distribution = df['Type'].value_counts().to_dict()
```

**Format:** Dictionary with type names as keys and counts as values

**Example:**
```python
{
    "Reactor": 5,
    "Heat Exchanger": 3,
    "Pump": 2
}
```

## Database Operations

### Saving New Dataset

**Process:**

1. Compute all analytics values
2. Create new EquipmentDataset instance
3. Populate all fields including CSV content as string
4. Save to database
5. Check total dataset count in database

### History Constraint Enforcement

**Requirement:** Maintain exactly last 5 datasets maximum

**Implementation:**

1. After saving new dataset, query database for all datasets ordered by `uploaded_at` descending
2. Count total datasets
3. If count > 5, delete oldest datasets beyond the 5th
4. Deletion targets datasets with earliest `uploaded_at` values

**Query Logic:**

```python
all_datasets = EquipmentDataset.objects.order_by('-uploaded_at')
if all_datasets.count() > 5:
    datasets_to_delete = all_datasets[5:]
    for dataset in datasets_to_delete:
        dataset.delete()
```

**Atomicity:** Perform within database transaction

### Retrieving Dataset

**By ID:**

```python
dataset = EquipmentDataset.objects.get(id=dataset_id)
```

**Error Handling:** Return 404 if dataset not found

**All History:**

```python
datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
```

**Order:** Most recent first

## Authentication Logic

### User Model

Use Django's built-in `User` model from `django.contrib.auth.models`

### Authentication Method

**Approach:** Token-based authentication using Django REST Framework's TokenAuthentication

**Setup:**

1. Enable `rest_framework.authtoken` in INSTALLED_APPS
2. Run migration to create token table
3. Configure DRF authentication classes

### Token Generation

**Process:**

1. User sends POST to `/api/login/` with username and password
2. Backend validates credentials using Django's `authenticate()`
3. If valid, retrieve or create token for user
4. Return token in JSON response

**Response Format:**

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Token Validation

**Process:**

1. Extract token from Authorization header: `Token <token_value>`
2. Lookup token in database
3. Retrieve associated user
4. Attach user to request object

**Protected Endpoints:** All endpoints except `/api/login/`

**Error Response:** 401 Unauthorized if token invalid or missing

## CSV Data Storage

**Storage Method:** Store complete CSV content as text in `csv_data` field

**Reason:** Enable regeneration of DataFrame for PDF reports without re-upload

**Retrieval:**

```python
csv_content = dataset.csv_data
df = pd.read_csv(StringIO(csv_content))
```

## Response Formatting

### Upload Success Response

**HTTP Status:** 201 Created

**JSON Structure (example based on sample dataset):**

```json
{
    "id": 1,
    "filename": "sample_equipment_data.csv",
    "uploaded_at": "2026-01-28T10:30:00Z",
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

**Note:** Actual values depend on uploaded dataset. Type distribution keys and counts are fully data-driven.

### History Response

**HTTP Status:** 200 OK

**JSON Structure:** Array of dataset objects

**Example (illustrative values):**

```json
[
    {
        "id": 5,
        "filename": "data5.csv",
        "uploaded_at": "2026-01-28T14:00:00Z",
        "total_count": 12,
        "avg_flowrate": 120.0,
        "avg_pressure": 16.0,
        "avg_temperature": 320.0,
        "type_distribution": {"Reactor": 6, "Pump": 6}
    },
    {
        "id": 4,
        "filename": "sample_equipment_data.csv",
        "uploaded_at": "2026-01-28T13:00:00Z",
        "total_count": 15,
        "avg_flowrate": 112.53,
        "avg_pressure": 14.37,
        "avg_temperature": 316.87,
        "type_distribution": {"Reactor": 5, "Heat Exchanger": 5, "Pump": 5}
    }
]
```

**Note:** Actual values depend on uploaded datasets. Counts, averages, and type distributions are computed from data.

## Error Response Format

**Standard Structure:**

```json
{
    "error": "Description of what went wrong"
}
```

**Common Errors:**

- 400: CSV validation failed, missing columns, invalid data types
- 401: Authentication failed, token invalid
- 404: Dataset not found
- 413: File too large
- 500: Server error during processing

## Data Validation Rules

### Equipment Name

- Type: String
- Required: Yes
- Constraints: Non-empty after stripping whitespace

### Type

- Type: String
- Required: Yes
- Constraints: Non-empty after stripping whitespace
- No predefined list of valid types; any non-empty string accepted

### Flowrate

- Type: Numeric (accepts integer or float, converted to float internally)
- Required: Yes
- Constraints: Must be convertible to float, no NaN
- Sample demonstrates integer values, but float values equally valid

### Pressure

- Type: Numeric (accepts integer or float, converted to float internally)
- Required: Yes
- Constraints: Must be convertible to float, no NaN
- Sample demonstrates float values with decimals

### Temperature

- Type: Numeric (accepts integer or float, converted to float internally)
- Required: Yes
- Constraints: Must be convertible to float, no NaN
- Sample demonstrates integer values, but float values equally valid

## Transaction Handling

### Upload Transaction

**Scope:** CSV parsing, analytics computation, database save, history cleanup

**Behavior:**

- Begin transaction before processing
- Commit only if all steps succeed
- Rollback on any error
- Return error response if rollback occurs

### Thread Safety

**Consideration:** Multiple simultaneous uploads must not corrupt history constraint

**Approach:** Use database-level locking or atomic operations for history cleanup
