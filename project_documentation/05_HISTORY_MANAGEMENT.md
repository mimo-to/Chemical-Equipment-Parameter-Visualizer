# Dataset History Management

## History Constraint

**Requirement:** Store last 5 uploaded datasets maximum

**Enforcement:** Automatic deletion of oldest datasets when limit exceeded

## Storage Model

### Database Table

**Model Name:** EquipmentDataset

**Ordering Field:** `uploaded_at` (DateTime with auto_now_add=True)

**Primary Key:** `id` (Integer, auto-increment)

### Stored Data Per Dataset

Each dataset record contains:

- Unique identifier
- Upload timestamp
- Original filename
- Summary statistics (total_count, averages, type_distribution)
- Complete CSV content as text

## History Management Algorithm

### On New Upload

**Step 1:** Process CSV and compute analytics

**Step 2:** Create new EquipmentDataset record

**Step 3:** Save record to database

**Step 4:** Query total count of datasets in database

**Step 5:** If count > 5, delete oldest datasets

### Deletion Logic

**Query for Deletion:**

```python
all_datasets = EquipmentDataset.objects.order_by('-uploaded_at')
datasets_to_keep = all_datasets[:5]
keep_ids = [d.id for d in datasets_to_keep]
EquipmentDataset.objects.exclude(id__in=keep_ids).delete()
```

**Alternative Approach:**

```python
all_datasets = EquipmentDataset.objects.order_by('-uploaded_at')
if all_datasets.count() > 5:
    datasets_to_delete = all_datasets[5:]
    for dataset in datasets_to_delete:
        dataset.delete()
```

### Deletion Criteria

**Identifier:** Oldest `uploaded_at` timestamp

**Count:** Delete all records beyond the 5 most recent

**Atomic Operation:** Deletion must complete before responding to upload request

[Clarification Added: History constraint enforcement is atomic with dataset creation to prevent race conditions during concurrent uploads]

**Enforcement Mechanism:** The save-and-cleanup operations execute within a single database transaction, ensuring the "last 5" constraint is maintained atomically even under concurrent upload requests.

## Ordering Specification

### Primary Order

**Field:** `uploaded_at`

**Direction:** Descending (most recent first)

**Query:**

```python
EquipmentDataset.objects.order_by('-uploaded_at')
```

### Tie-Breaking

**Scenario:** Two uploads with identical timestamps (unlikely but possible)

**Resolution:** Use `id` as secondary sort (higher ID = more recent)

**Query:**

```python
EquipmentDataset.objects.order_by('-uploaded_at', '-id')
```

## History Retrieval

### Get Last 5 Datasets

**Endpoint:** GET /api/history/

**Query:**

```python
datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
```

**Result:** List of 0 to 5 dataset objects

### Response Format

Array of dataset objects in descending chronological order:

```json
[
    {
        "id": 5,
        "filename": "most_recent.csv",
        "uploaded_at": "2026-01-28T14:00:00.000Z",
        "total_count": 10,
        "avg_flowrate": 120.0,
        "avg_pressure": 16.0,
        "avg_temperature": 320.0,
        "type_distribution": {"Reactor": 6, "Pump": 4}
    },
    {
        "id": 4,
        "filename": "second_most_recent.csv",
        "uploaded_at": "2026-01-28T13:00:00.000Z",
        "total_count": 8,
        "avg_flowrate": 110.0,
        "avg_pressure": 14.0,
        "avg_temperature": 300.0,
        "type_distribution": {"Reactor": 5, "Heat Exchanger": 3}
    }
]
```

## Concurrency Handling

### Simultaneous Uploads

**Scenario:** Two users upload CSV files at the same time

**Challenge:** Both uploads trigger history cleanup

**Solution:** Database transaction isolation

### Transaction Scope

**Begin Transaction:** Before saving new dataset

**Operations Within Transaction:**

1. Save new dataset
2. Query all datasets
3. Delete old datasets if count > 5

**Commit Transaction:** After all operations complete

**Rollback:** If any operation fails

### Locking Strategy

**Approach 1:** Database row locking

```python
with transaction.atomic():
    new_dataset.save()
    all_datasets = EquipmentDataset.objects.select_for_update().order_by('-uploaded_at')
    if all_datasets.count() > 5:
        EquipmentDataset.objects.exclude(
            id__in=[d.id for d in all_datasets[:5]]
        ).delete()
```

**Approach 2:** Serializable isolation level

Configure Django to use serializable isolation for dataset operations.

## Edge Cases

### Case 1: First Upload

**State:** Database is empty

**Behavior:**

- Save new dataset
- Count = 1
- No deletion occurs

**Result:** Database contains 1 dataset

### Case 2: Fifth Upload

**State:** Database has 4 datasets

**Behavior:**

- Save new dataset
- Count = 5
- No deletion occurs

**Result:** Database contains 5 datasets

### Case 3: Sixth Upload

**State:** Database has 5 datasets

**Behavior:**

- Save new dataset
- Count = 6
- Delete oldest dataset (uploaded first)

**Result:** Database contains 5 datasets (most recent 5)

### Case 4: Tenth Upload

**State:** Database has 5 datasets

**Behavior:**

- Save new dataset
- Count = 6
- Delete oldest dataset

**Result:** Database contains 5 datasets (uploads 6-10 retained)

### Case 5: Simultaneous Sixth and Seventh Upload

**State:** Database has 5 datasets

**Scenario:** Two uploads start simultaneously

**Expected Behavior:**

- Upload 6 completes first: saves, deletes dataset 1
- Upload 7 completes second: saves, deletes dataset 2
- Final state: Database contains datasets 3, 4, 5, 6, 7

**Requirement:** Transaction isolation prevents race condition

## Deletion Confirmation

### Verification After Deletion

**Query:**

```python
remaining_count = EquipmentDataset.objects.count()
assert remaining_count <= 5
```

**Timing:** Verify before transaction commit

**Action on Failure:** Rollback transaction, return 500 error

## History Display Requirements

### Web Frontend

**Display:** List or table showing last 5 datasets

**Columns:**

- Filename
- Upload timestamp (formatted)
- Total count
- Summary statistics

**Interaction:** Click to view details or generate report

### Desktop Frontend

**Display:** List widget or table showing last 5 datasets

**Columns:** Same as web frontend

**Interaction:** Select to view details or generate report

## Dataset Deletion Impact

### On PDF Generation

**Scenario:** User requests PDF for deleted dataset

**Response:** 404 Not Found

**Error Message:** "Dataset not found"

### On Visualization

**Scenario:** User requests visualization for deleted dataset

**Response:** 404 Not Found

**Error Message:** "Dataset not found"

### Client Handling

**Frontend Behavior:**

- Refresh history list after each upload
- Handle 404 errors gracefully
- Inform user that old datasets are automatically deleted

## Timestamp Precision

### Storage

**Format:** Django DateTimeField with auto_now_add=True

**Precision:** Microseconds (database dependent)

**Timezone:** UTC

### Display

**Format:** ISO 8601 string

**Example:** "2026-01-28T14:00:00.123456Z"

**Rounding:** No rounding required for display

## Data Retention Policy

**Policy:** Keep only last 5 datasets

**Purpose:** Limit storage usage as specified in requirements

**User Notification:** Not required by specification, but recommended

**Data Export:** Users should download important reports before they expire

## Testing Scenarios

### Scenario 1: Sequential Uploads

Upload 10 CSV files sequentially (including sample_equipment_data.csv for demo), verify:

- After upload 5: 5 datasets in database
- After upload 6: 5 datasets (1st deleted)
- After upload 10: 5 datasets (1st-5th deleted)
- Each dataset shows computed total_count matching its actual row count

### Scenario 2: Concurrent Uploads

Upload 2 CSV files simultaneously when database has 5 datasets, verify:

- Both uploads succeed
- Database contains exactly 5 datasets
- Oldest 2 datasets deleted

### Scenario 3: History Retrieval

After 7 uploads, retrieve history, verify:

- Response contains exactly 5 datasets
- Datasets are uploads 3-7
- Ordered by upload time descending

## Performance Considerations

### Deletion Performance

**Operation:** Delete old datasets

**Frequency:** After each upload when count > 5

**Cost:** Single DELETE query affecting 1-N rows

**Acceptable:** Yes for constraint of 5 datasets

### Query Performance

**Index:** Index on `uploaded_at` field improves ORDER BY performance

**Expected Size:** Maximum 5 rows in table

**Query Cost:** Negligible for small dataset count

## Cleanup on Application Reset

### Development Reset

**Command:** Django's flush or migrate --fake-initial

**Effect:** Deletes all datasets

**Required:** When resetting development database

### Production Deployment

**Migration:** Ensure model migration creates table correctly

**Initial State:** Empty database (0 datasets)

**First Upload:** Follows normal flow
