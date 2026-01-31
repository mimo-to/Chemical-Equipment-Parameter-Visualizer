# Model Behavior and Output Rules

## Core Principle

When generating code for this project, the model must produce output that appears naturally written by a human developer, not by an AI system.

## Code Generation Rules

### Natural Human Style

**Characteristics:**

- Concise variable names without excessive descriptiveness
- Straightforward logic without over-explanation
- Standard idioms and patterns for the language
- Minimal abstraction appropriate to problem size
- No defensive programming beyond reasonable error handling

**Anti-Patterns to Avoid:**

- Variable names like `dataFromServerResponseForEquipmentList`
- Functions named `handleProcessingOfUserInputData`
- Excessive validation of every possible edge case
- Wrapper functions around standard library calls
- Comments explaining obvious operations

### Naming Conventions

**Python Variables:**

```python
df
token
dataset
history
response
avg_flowrate
type_dist
```

**NOT:**

```python
dataFrame
authenticationToken
datasetObjectFromDatabase
historyOfDatasets
responseFromAPICall
averageFlowrateValue
typeDistributionDictionary
```

**JavaScript Variables:**

```javascript
data
user
token
datasets
chartData
```

**NOT:**

```javascript
dataFromAPI
currentlyAuthenticatedUser
authenticationTokenString
arrayOfDatasetObjects
chartDataForVisualization
```

### Function Structure

**Preferred:**

```python
def compute_averages(df):
    return {
        'flowrate': round(df['Flowrate'].mean(), 2),
        'pressure': round(df['Pressure'].mean(), 2),
        'temperature': round(df['Temperature'].mean(), 2)
    }
```

**Avoid:**

```python
def compute_and_return_average_values_for_all_numeric_columns(dataframe_object):
    average_flowrate_value = dataframe_object['Flowrate'].mean()
    rounded_average_flowrate = round(average_flowrate_value, 2)
    
    average_pressure_value = dataframe_object['Pressure'].mean()
    rounded_average_pressure = round(average_pressure_value, 2)
    
    average_temperature_value = dataframe_object['Temperature'].mean()
    rounded_average_temperature = round(average_temperature_value, 2)
    
    result_dictionary = {
        'flowrate': rounded_average_flowrate,
        'pressure': rounded_average_pressure,
        'temperature': rounded_average_temperature
    }
    
    return result_dictionary
```

## Comment Prohibition

### Absolute Rules

**NEVER generate:**

- Inline comments explaining code logic
- Docstrings explaining function behavior
- Block comments describing sections
- TODO or FIXME comments
- Header comments in files
- Comments explaining imports
- Comments explaining variable assignments
- Comments explaining return statements

### Exception Cases (Rare)

**Only if absolutely necessary:**

- MIT/BSD license header if required
- Configuration format notes in config files (minimal)
- Regex pattern explanation if pattern is genuinely complex

**Even then:**

- Keep to absolute minimum
- Prefer self-documenting code
- Use clear variable names instead

### Examples

**WRONG:**

```python
class EquipmentDataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    total_count = models.IntegerField()
```

**CORRECT:**

```python
class EquipmentDataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    total_count = models.IntegerField()
```

**WRONG:**

```javascript
const uploadCSV = async (file, token) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload/', {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`
        },
        body: formData
    });
    
    return response.json();
};
```

**CORRECT:**

```javascript
const uploadCSV = async (file, token) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload/', {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`
        },
        body: formData
    });
    
    return response.json();
};
```

## Code Organization

### File-Level Organization

**Django views.py:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentDataset
from .serializers import DatasetSerializer
import pandas as pd

class UploadView(APIView):
    def post(self, request):
        pass

class HistoryView(APIView):
    def get(self, request):
        pass
```

**NOT:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentDataset
from .serializers import DatasetSerializer
import pandas as pd

class UploadView(APIView):
    def post(self, request):
        pass

class HistoryView(APIView):
    def get(self, request):
        pass
```

### Import Organization

**Standard Order:**

```python
import os
import json
from datetime import datetime

import pandas as pd
from django.db import models
from rest_framework.views import APIView

from .models import EquipmentDataset
from .utils import compute_statistics
```

**Group Separation:** Single blank line between groups

**Within Group:** Alphabetical order

## Error Handling

### Appropriate Error Handling

```python
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    
    if not file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=400)
    
    try:
        df = pd.read_csv(file)
    except Exception:
        return Response({'error': 'Invalid CSV format'}, status=400)
    
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    if not all(col in df.columns for col in required_columns):
        return Response({'error': 'Missing required columns'}, status=400)
    
    return Response({'success': True})
```

### Excessive Error Handling (Avoid)

```python
def upload_csv(request):
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
    try:
        file = request.FILES['file']
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
    try:
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
```

## Logic Simplicity

### Prefer Direct Logic

```python
def enforce_history_limit():
    datasets = EquipmentDataset.objects.order_by('-uploaded_at')
    if datasets.count() > 5:
        datasets[5:].delete()
```

### Avoid Over-Abstraction

```python
class HistoryManager:
    MAX_HISTORY_SIZE = 5
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def enforce_limit(self):
        queryset = self.get_ordered_queryset()
        excess_count = self.calculate_excess_count(queryset)
        if excess_count > 0:
            self.delete_excess_items(queryset, excess_count)
    
    def get_ordered_queryset(self):
        return self.model_class.objects.order_by('-uploaded_at')
    
    def calculate_excess_count(self, queryset):
        return max(0, queryset.count() - self.MAX_HISTORY_SIZE)
    
    def delete_excess_items(self, queryset, count):
        queryset[self.MAX_HISTORY_SIZE:].delete()

history_manager = HistoryManager(EquipmentDataset)
history_manager.enforce_limit()
```

## React Component Structure

### Functional Components

```javascript
function Upload({ token, onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };
    
    const handleUpload = async () => {
        if (!file) return;
        
        setUploading(true);
        setError(null);
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/upload/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`
                },
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                onUploadSuccess(data);
            } else {
                const error = await response.json();
                setError(error.error);
            }
        } catch (err) {
            setError('Network error');
        } finally {
            setUploading(false);
        }
    };
    
    return (
        <div>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!file || uploading}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>
            {error && <div className="error">{error}</div>}
        </div>
    );
}
```

### Hook Usage

**Appropriate:**

- useState for component state
- useEffect for side effects
- useCallback for memoized callbacks (only if needed)

**Avoid Unnecessary:**

- useMemo unless demonstrable performance issue
- useRef unless accessing DOM or persisting values
- Custom hooks for simple logic

## Database Queries

### Direct and Clear

```python
def get_history():
    return EquipmentDataset.objects.order_by('-uploaded_at')[:5]

def get_dataset(dataset_id):
    return EquipmentDataset.objects.get(id=dataset_id)
```

### Avoid Query Builders for Simple Cases

```python
class DatasetQueryBuilder:
    def __init__(self):
        self.query = EquipmentDataset.objects
    
    def order_by_recent(self):
        self.query = self.query.order_by('-uploaded_at')
        return self
    
    def limit(self, count):
        self.query = self.query[:count]
        return self
    
    def execute(self):
        return self.query

datasets = DatasetQueryBuilder().order_by_recent().limit(5).execute()
```

## API Response Formatting

### Serializers (Django)

```python
class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 
                  'type_distribution']
```

### Manual Formatting

```python
def format_dataset_response(dataset):
    return {
        'id': dataset.id,
        'filename': dataset.filename,
        'uploaded_at': dataset.uploaded_at.isoformat(),
        'total_count': dataset.total_count,
        'avg_flowrate': dataset.avg_flowrate,
        'avg_pressure': dataset.avg_pressure,
        'avg_temperature': dataset.avg_temperature,
        'type_distribution': dataset.type_distribution
    }
```

**Both acceptable, prefer serializers for consistency**

## Configuration Values

### Settings Location

**Django settings.py:**

```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### Hardcoded Values (Acceptable for Prototype)

```python
BASE_URL = 'http://localhost:8000'
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_HISTORY_SIZE = 5
```

### Avoid Configuration Overengineering

**Not needed for this project:**

- Environment-specific config files
- Complex configuration classes
- Config validation frameworks
- Dynamic configuration loading

## Testing Code Style

**If writing tests (not required):**

```python
def test_upload_csv():
    client = APIClient()
    client.force_authenticate(user=test_user)
    
    with open('test.csv', 'rb') as f:
        response = client.post('/api/upload/', {'file': f})
    
    assert response.status_code == 201
    assert 'total_count' in response.data
```

**No comments in tests either**

## Output Validation

### Before Submitting Code

**Check for:**

- [ ] No comments anywhere
- [ ] Natural variable/function names
- [ ] Straightforward logic flow
- [ ] Appropriate error handling (not excessive)
- [ ] Standard idioms for language
- [ ] Minimal abstraction
- [ ] Clean, readable code

### Red Flags

**If code has these, revise:**

- Comments explaining code
- Variable names longer than 25 characters
- More than 3 levels of nesting
- Functions longer than 100 lines without clear reason
- Abstract base classes for single implementation
- Factory patterns for simple object creation
- Observer patterns for simple callbacks

## Language-Specific Idioms

### Python

**Use:**

- List comprehensions for simple transformations
- Context managers (with statements)
- Dictionary/set comprehensions
- f-strings for formatting
- Built-in functions (map, filter, zip) when clear

**Avoid:**

- Lambda functions beyond simple callbacks
- Metaclasses
- Decorators beyond standard library
- Magic methods unless necessary

### JavaScript/React

**Use:**

- Arrow functions
- Destructuring
- Spread operator
- Template literals
- Async/await
- Array methods (map, filter, reduce)

**Avoid:**

- Prototype manipulation
- eval()
- with statement
- Complex this binding
- Excessive chaining

### SQL/ORM

**Use:**

- Django ORM query methods
- select_related/prefetch_related only if N+1 problem
- F expressions for database-level operations
- Standard filtering and ordering

**Avoid:**

- Raw SQL unless absolutely necessary
- Complex query annotations for simple cases
- Over-optimization without measurement

## Final Quality Check

### Code Should Read Like

Human developer who:

- Knows the language well
- Writes clean code
- Doesn't over-explain
- Uses standard patterns
- Keeps things simple
- Focuses on clarity

### Code Should NOT Read Like

AI system that:

- Explains every step
- Uses excessively long names
- Adds unnecessary abstraction
- Includes defensive programming everywhere
- Anticipates unstated requirements
- Over-documents obvious operations

## Completion Criteria

Code is complete when:

1. All specified features work correctly
2. No comments present anywhere
3. Style is natural and human-like
4. Logic is straightforward and clear
5. Error handling is appropriate
6. File organization is clean
7. Tests pass (if written)
8. README explains setup clearly

Code should be ready for immediate evaluation by technical reviewers who expect clean, professional, human-written code.
