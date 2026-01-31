# Analytics Computations and Formulas

## Required Analytics

The backend must compute exactly these analytics for each uploaded dataset:

1. Total Count
2. Average Flowrate
3. Average Pressure
4. Average Temperature
5. Type Distribution

## Data Preparation

### Input Data

**Source:** CSV file with required columns

**Required Columns:**

- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

### Data Cleaning Steps

**Step 1: Load CSV**

Use Pandas to read CSV into DataFrame.

**Step 2: Validate Columns**

Verify all required columns exist with exact names (case-sensitive).

**Step 3: Type Conversion**

Convert numeric columns to float:

```python
df['Flowrate'] = pd.to_numeric(df['Flowrate'], errors='coerce')
df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
```

**Step 4: Remove Invalid Rows**

Drop rows with NaN values in any column:

```python
df = df.dropna()
```

**Step 5: Trim Strings**

Remove leading/trailing whitespace from string columns:

```python
df['Equipment Name'] = df['Equipment Name'].str.strip()
df['Type'] = df['Type'].str.strip()
```

**Step 6: Validate Non-Empty**

After cleaning, verify DataFrame has at least 1 row. If empty, return error.

## Computation 1: Total Count

### Definition

Number of equipment entries after data cleaning.

### Formula

```
total_count = number of rows in cleaned DataFrame
```

### Implementation

```python
total_count = len(df)
```

### Constraints

- Must be integer
- Must be greater than 0 after cleaning
- Represents count of valid equipment rows only

### Example

If CSV has 10 rows initially and 2 rows are removed due to invalid data:

```
total_count = 8
```

## Computation 2: Average Flowrate

### Definition

Arithmetic mean of all Flowrate values in cleaned dataset.

### Formula

```
avg_flowrate = sum(Flowrate values) / count(Flowrate values)
```

### Implementation

```python
avg_flowrate = df['Flowrate'].mean()
```

### Rounding

Round result to 2 decimal places:

```python
avg_flowrate = round(df['Flowrate'].mean(), 2)
```

### Constraints

- Must be numeric (float)
- Must be rounded to exactly 2 decimal places
- Cannot be NaN (ensured by data cleaning)

### Example (Illustrative)

Given Flowrate values: [120, 80, 150, 95]

```
avg_flowrate = (120 + 80 + 150 + 95) / 4 = 111.25
Rounded: 111.25
```

Note: This is an illustrative example. Actual computations depend on uploaded dataset content. Sample dataset contains arbitrary numeric values; system handles any valid numeric input.

## Computation 3: Average Pressure

### Definition

Arithmetic mean of all Pressure values in cleaned dataset.

### Formula

```
avg_pressure = sum(Pressure values) / count(Pressure values)
```

### Implementation

```python
avg_pressure = df['Pressure'].mean()
```

### Rounding

Round result to 2 decimal places:

```python
avg_pressure = round(df['Pressure'].mean(), 2)
```

### Constraints

- Must be numeric (float)
- Must be rounded to exactly 2 decimal places
- Cannot be NaN (ensured by data cleaning)

### Example

Given Pressure values: [15.2, 10.5, 20.0, 12.8]

```
avg_pressure = (15.2 + 10.5 + 20.0 + 12.8) / 4 = 14.625
Rounded: 14.63
```

## Computation 4: Average Temperature

### Definition

Arithmetic mean of all Temperature values in cleaned dataset.

### Formula

```
avg_temperature = sum(Temperature values) / count(Temperature values)
```

### Implementation

```python
avg_temperature = df['Temperature'].mean()
```

### Rounding

Round result to 2 decimal places:

```python
avg_temperature = round(df['Temperature'].mean(), 2)
```

### Constraints

- Must be numeric (float)
- Must be rounded to exactly 2 decimal places
- Cannot be NaN (ensured by data cleaning)

### Example (Illustrative)

Given Temperature values: [350, 280, 300, 320]

```
avg_temperature = (350 + 280 + 300 + 320) / 4 = 312.5
Rounded: 312.50
```

Note: This is an illustrative example. Actual average depends on dataset content.

## Computation 5: Type Distribution

### Definition

Count of equipment entries for each unique Type value.

### Formula

For each unique value in Type column:

```
count_for_type = number of rows where Type equals that value
```

### Implementation

```python
type_distribution = df['Type'].value_counts().to_dict()
```

### Output Format

Dictionary mapping Type name to count:

```python
{
    "Reactor": 4,
    "Heat Exchanger": 3,
    "Pump": 3
}
```

### Constraints

- Must be dictionary (object in JSON)
- Keys are unique Type values as strings
- Values are integer counts
- Sum of all counts equals total_count
- Only includes types present in dataset (no zero counts)

### Example (Illustrative)

Given Type column values (example with 15 rows):

```
["Reactor", "Heat Exchanger", "Pump", "Reactor", "Heat Exchanger", "Pump", "Reactor", "Heat Exchanger", "Pump", "Reactor", "Heat Exchanger", "Pump", "Reactor", "Heat Exchanger", "Pump"]
```

Result:

```python
{
    "Reactor": 5,
    "Heat Exchanger": 5,
    "Pump": 5
}
```

Verification: 5 + 5 + 5 = 15 (total_count)

**Important:** Type names, counts, and distribution are fully data-driven. Sample demonstrates equal distribution, but actual datasets may have any distribution. System handles arbitrary number of unique types with any frequency.

## Validation Rules

### Pre-Computation Validation

**Rule 1:** CSV must have all required columns

**Action if violated:** Return 400 error listing missing columns

**Rule 2:** Numeric columns must be convertible to float

**Action if violated:** Return 400 error specifying row and column with invalid value

**Rule 3:** After cleaning, at least 1 row must remain

**Action if violated:** Return 400 error indicating no valid data

### Post-Computation Validation

**Rule 4:** All averages must be finite numbers (not NaN, not infinite)

**Action if violated:** Return 500 error (indicates data cleaning failure)

**Rule 5:** Type distribution sum must equal total_count

**Action if violated:** Return 500 error (indicates computation error)

## Edge Cases

### Single Row Dataset

**Behavior:**

- total_count = 1
- Averages = values from that single row
- Type distribution = {type_from_row: 1}

**Valid:** Yes

### All Same Type

**Behavior:**

- Type distribution has single entry
- Example: {"Reactor": 10}

**Valid:** Yes

### Identical Values in Numeric Columns

**Behavior:**

- Average equals the repeated value
- Example: All Flowrate = 100.0, then avg_flowrate = 100.0

**Valid:** Yes

### Very Large Numbers

**Behavior:**

- Python float handles up to ~10^308
- Averages computed normally
- Round to 2 decimal places regardless of magnitude

**Valid:** Yes, within float range

### Negative Values

**Behavior:**

- Accepted if parseable as float
- Included in average calculations
- No domain validation on physical meaning

**Valid:** Yes (task does not specify positive-only constraint)

### Zero Values

**Behavior:**

- Treated as valid numeric values
- Included in average calculations

**Valid:** Yes

## Computation Order

**Sequence:**

1. Load and validate CSV structure
2. Clean data (type conversion, drop NaN, trim strings)
3. Validate non-empty result
4. Compute total_count
5. Compute avg_flowrate
6. Compute avg_pressure
7. Compute avg_temperature
8. Compute type_distribution
9. Validate computation results
10. Store in database

**Dependency:** All computations depend on cleaned DataFrame

**Independence:** Computations can be performed in parallel after cleaning

## Storage Requirements

### Database Field Types

- `total_count`: Integer field
- `avg_flowrate`: Float field (Django FloatField)
- `avg_pressure`: Float field (Django FloatField)
- `avg_temperature`: Float field (Django FloatField)
- `type_distribution`: JSON field (Django JSONField)

### Precision Preservation

**Averages:** Store as computed (2 decimal places already applied)

**Type Distribution:** Store complete dictionary

**No Additional Rounding:** Values stored are final computed values

## API Response Format

### Summary Statistics Object (Illustrative Example)

```json
{
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

Note: Values shown are based on sample dataset. Actual values are computed from uploaded data.

### Visualization Data Format (Illustrative Example)

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

Note: Type labels and counts vary by dataset. Array lengths are data-driven.

## Statistical Assumptions

**Mean vs Median:** Use arithmetic mean only, no median computation required

**Outlier Handling:** No outlier detection or removal, include all valid values

**Weighting:** Simple average, no weighted calculations

**Distribution:** No assumption about data distribution (normal, etc.)

## Performance Considerations

### Large CSV Files

**Expected Size:** Up to 10MB

**Row Estimate:** Potentially thousands of rows

**Optimization:** Pandas operations are vectorized, efficient for typical dataset sizes

### Memory Usage

**CSV Storage:** Store complete CSV content in database as text

**Memory Overhead:** Acceptable for datasets under 10MB

**Streaming:** Not required for specified constraints
