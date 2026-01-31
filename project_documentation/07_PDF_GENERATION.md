# PDF Report Generation

## Requirement

Generate downloadable PDF report containing summary statistics for a dataset.

## Endpoint

### GET /api/report/<int:id>/

**Purpose:** Generate and download PDF report for specified dataset

**Authentication Required:** Yes

**URL Parameter:** `id` - Integer, dataset identifier

## PDF Generation Library

**Recommended:** ReportLab

**Installation:** `pip install reportlab`

**Reason:** Pure Python, widely used, suitable for programmatic PDF generation

**Alternative:** fpdf, WeasyPrint (not recommended for simplicity)

## Report Content

### Required Elements

The PDF report must include:

1. Report title
2. Dataset information (filename, upload timestamp)
3. Summary statistics
4. Type distribution data

### Title Section

**Content:** "Chemical Equipment Analysis Report"

**Formatting:** Large font, bold, centered

**Position:** Top of page

### Dataset Information Section

**Content:**

- Filename: [original filename]
- Upload Date: [formatted timestamp]
- Dataset ID: [numeric id]

**Formatting:** Regular font, left-aligned

**Position:** Below title

### Summary Statistics Section

**Content:**

- Total Equipment Count: [integer]
- Average Flowrate: [float with 2 decimals]
- Average Pressure: [float with 2 decimals]
- Average Temperature: [float with 2 decimals]

**Formatting:** Regular font, left-aligned or in table format

**Position:** Below dataset information

### Type Distribution Section

**Content:** Table showing equipment types and counts

**Columns:**

- Equipment Type
- Count

**Rows:** One row per unique type

**Example:**

```
Equipment Type    | Count
------------------|------
Reactor           | 4
Heat Exchanger    | 3
Pump              | 3
```

**Formatting:** Table with borders, headers in bold

**Position:** Below summary statistics

## PDF Generation Process

### Step 1: Retrieve Dataset

Query database for dataset with specified ID:

```python
dataset = EquipmentDataset.objects.get(id=dataset_id)
```

**Error Handling:** If not found, return 404 Not Found

### Step 2: Create PDF Document

Initialize ReportLab PDF canvas or document:

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

buffer = BytesIO()
pdf = canvas.Canvas(buffer, pagesize=letter)
```

### Step 3: Add Content

**Add Title:**

```python
pdf.setFont("Helvetica-Bold", 20)
pdf.drawCentredString(300, 750, "Chemical Equipment Analysis Report")
```

**Add Dataset Information:**

```python
pdf.setFont("Helvetica", 12)
pdf.drawString(50, 700, f"Filename: {dataset.filename}")
pdf.drawString(50, 680, f"Upload Date: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
pdf.drawString(50, 660, f"Dataset ID: {dataset.id}")
```

**Add Summary Statistics:**

```python
pdf.drawString(50, 620, f"Total Equipment Count: {dataset.total_count}")
pdf.drawString(50, 600, f"Average Flowrate: {dataset.avg_flowrate}")
pdf.drawString(50, 580, f"Average Pressure: {dataset.avg_pressure}")
pdf.drawString(50, 560, f"Average Temperature: {dataset.avg_temperature}")
```

**Add Type Distribution:**

Create table with type names and counts from `dataset.type_distribution` JSON field.

### Step 4: Finalize PDF

```python
pdf.showPage()
pdf.save()
```

### Step 5: Return Response

```python
buffer.seek(0)
response = HttpResponse(buffer, content_type='application/pdf')
response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
return response
```

## Response Specification

### Success Response

**Status Code:** 200 OK

**Headers:**

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="report_<dataset_id>.pdf"
```

**Body:** Binary PDF file content

### Filename Format

**Pattern:** `report_<dataset_id>.pdf`

**Examples:**

- Dataset ID 1: `report_1.pdf`
- Dataset ID 42: `report_42.pdf`

### Error Responses

**Dataset Not Found:**

**Status Code:** 404 Not Found

**Body:**

```json
{
    "error": "Dataset not found"
}
```

**PDF Generation Failure:**

**Status Code:** 500 Internal Server Error

**Body:**

```json
{
    "error": "Failed to generate PDF report"
}
```

## Frontend Handling

### Web Frontend (React)

**Step 1:** User clicks "Generate Report" button for a dataset

**Step 2:** Send GET request to `/api/report/<id>/` with authentication token

**Step 3:** Receive PDF as blob

**Step 4:** Create download link and trigger download

```javascript
const response = await fetch(`/api/report/${datasetId}/`, {
    headers: {
        'Authorization': `Token ${token}`
    }
});
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `report_${datasetId}.pdf`;
a.click();
```

### Desktop Frontend (PyQt5)

**Step 1:** User clicks "Generate Report" button for a dataset

**Step 2:** Send GET request to `/api/report/<id>/` with authentication token

**Step 3:** Receive PDF content

**Step 4:** Open save file dialog

**Step 5:** Write PDF content to selected file location

```python
response = requests.get(
    f'http://localhost:8000/api/report/{dataset_id}/',
    headers={'Authorization': f'Token {token}'}
)

if response.status_code == 200:
    filepath, _ = QFileDialog.getSaveFileName(
        self, 
        "Save Report", 
        f"report_{dataset_id}.pdf", 
        "PDF Files (*.pdf)"
    )
    if filepath:
        with open(filepath, 'wb') as f:
            f.write(response.content)
```

## PDF Formatting Guidelines

### Page Size

**Standard:** Letter (8.5 x 11 inches)

**Alternative:** A4 (acceptable if preferred)

**ReportLab:** `letter` or `A4` from `reportlab.lib.pagesizes`

### Margins

**Top:** 50-100 points

**Left/Right:** 50-72 points

**Bottom:** 50 points

### Fonts

**Title:** Helvetica-Bold, 18-24 points

**Section Headers:** Helvetica-Bold, 14-16 points

**Body Text:** Helvetica, 10-12 points

**Table Text:** Helvetica, 10-11 points

### Colors

**Not Required:** Black text on white background is sufficient

**Optional:** May add colors for headers or table borders

### Layout

**Single Page:** All content fits on one page for typical datasets

**Multiple Pages:** If type distribution is large, content may span pages

**Overflow Handling:** Ensure table continues on next page if needed

## Data Formatting in PDF

### Timestamp Format

**Source:** `dataset.uploaded_at` (DateTime object)

**Display Format:** `YYYY-MM-DD HH:MM:SS`

**Example:** `2026-01-28 14:30:00`

**Timezone:** Display in UTC or convert to local (UTC is simpler)

### Numeric Formatting

**Integers:** Display as-is (e.g., `10`)

**Floats:** Display with 2 decimal places (e.g., `115.56`)

**Alignment:** Right-align numeric columns in tables

### Type Distribution Table

**Sorting:** Alphabetical by type name or by count descending

**Preferred:** Count descending (most common types first)

**Implementation:**

```python
sorted_types = sorted(
    dataset.type_distribution.items(), 
    key=lambda x: x[1], 
    reverse=True
)
```

## Error Handling During Generation

### Type Distribution Empty

**Should Not Occur:** Data validation ensures at least one type exists

**Fallback:** Display "No data" if somehow empty

### Very Long Type Names

**Handling:** Truncate or wrap text to fit table width

**Alternative:** Adjust column widths dynamically

### Large Type Distribution

**Handling:** If many types, table may extend across pages

**ReportLab:** Handles multi-page tables automatically with proper setup

## Performance Considerations

### Generation Time

**Expected:** Less than 1 second for typical dataset

**Acceptable:** Up to 3-5 seconds for large type distributions

**Optimization:** Not critical for specified requirements

### Memory Usage

**Buffering:** Use BytesIO to generate PDF in memory

**Size:** PDF file size typically under 100 KB

**Acceptable:** No streaming required for small PDFs

## Testing PDF Generation

### Test Case 1: Basic Report

**Input:** Dataset with 10 equipment, 3 types

**Expected Output:** PDF with all sections, readable content

### Test Case 2: Single Type

**Input:** Dataset with all equipment of one type

**Expected Output:** Type distribution table with single row

### Test Case 3: Many Types

**Input:** Dataset with 20 different types

**Expected Output:** PDF with all types listed, possibly multiple pages

### Test Case 4: Dataset Not Found

**Input:** Request for non-existent dataset ID

**Expected Output:** 404 error response

## Optional Enhancements

### Not Required but Acceptable

- Page numbers
- Generation timestamp
- Logo or branding
- Charts or graphs embedded in PDF
- Color-coded sections
- Additional statistics

**Note:** These are not required by task specification. Basic report with required elements is sufficient.

## ReportLab Code Structure Example

### Minimal Implementation Pattern

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generate_pdf_report(dataset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 750, "Chemical Equipment Analysis Report")
    
    pdf.setFont("Helvetica", 12)
    y_position = 700
    pdf.drawString(50, y_position, f"Filename: {dataset.filename}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Upload Date: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Dataset ID: {dataset.id}")
    
    y_position -= 40
    pdf.drawString(50, y_position, f"Total Equipment Count: {dataset.total_count}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Average Flowrate: {dataset.avg_flowrate}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Average Pressure: {dataset.avg_pressure}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Average Temperature: {dataset.avg_temperature}")
    
    y_position -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position, "Type Distribution")
    y_position -= 20
    
    pdf.setFont("Helvetica", 11)
    for type_name, count in sorted(dataset.type_distribution.items(), key=lambda x: x[1], reverse=True):
        pdf.drawString(50, y_position, f"{type_name}: {count}")
        y_position -= 15
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer
```

## Integration with API View

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

class GenerateReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, dataset_id):
        try:
            dataset = EquipmentDataset.objects.get(id=dataset_id)
        except EquipmentDataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            pdf_buffer = generate_pdf_report(dataset)
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{dataset_id}.pdf"'
            return response
        except Exception as e:
            return Response(
                {"error": "Failed to generate PDF report"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```
