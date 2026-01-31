# Desktop Frontend Interaction Rules (PyQt5)

## Technology Stack

**Framework:** PyQt5

**Charting Library:** Matplotlib

**HTTP Client:** requests library

**Python Version:** Python 3.8+

## Application Structure

### File Organization

```
desktop/
├── main.py
├── ui/
│   ├── main_window.py
│   ├── login_dialog.py
│   ├── upload_widget.py
│   ├── charts_widget.py
│   └── history_widget.py
└── services/
    └── api_client.py
```

**main.py:** Application entry point, QApplication initialization

**main_window.py:** Main window class with menus and central widget

**login_dialog.py:** Login dialog for authentication

**upload_widget.py:** CSV file selection and upload interface

**charts_widget.py:** Matplotlib charts embedded in PyQt5

**history_widget.py:** List or table of past datasets

**api_client.py:** API communication logic

## Application Initialization

### Main Entry Point

```python
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

### Window Configuration

**Title:** "Chemical Equipment Visualizer"

**Initial Size:** 1000x700 pixels (or similar)

**Layout:** QVBoxLayout or QHBoxLayout for organizing widgets

**Menu Bar:** File menu with Exit option

## Authentication Flow

### Login Dialog

**Type:** QDialog (modal)

**Display Timing:** On application startup or when token invalid

**Elements:**

- Username QLineEdit
- Password QLineEdit (with echo mode Password)
- Login QPushButton
- Cancel QPushButton (optional, closes application)
- Status QLabel for error messages

### Login Process

**Step 1:** Display login dialog on startup

**Step 2:** User enters credentials and clicks Login

**Step 3:** Send POST to `/api/login/`

```python
import requests

response = requests.post(
    'http://localhost:8000/api/login/',
    json={'username': username, 'password': password}
)
```

**Step 4:** Handle response

**Success (200):**

```python
data = response.json()
token = data['token']
self.token = token
self.login_dialog.accept()
```

**Failure (401, 400):**

```python
error = response.json().get('error', 'Login failed')
self.status_label.setText(error)
```

### Token Storage

**Method:** Store in memory as instance variable

**Alternative:** Store in QSettings for session persistence

**In-Memory:**

```python
self.auth_token = None

def set_token(self, token):
    self.auth_token = token
```

**QSettings:**

```python
from PyQt5.QtCore import QSettings

settings = QSettings('FOSSEE', 'EquipmentVisualizer')
settings.setValue('auth_token', token)

token = settings.value('auth_token', None)
```

### Session Management

**On Successful Login:**

- Close login dialog
- Enable main window widgets
- Store token
- Proceed to upload interface

**On 401 Error During Operation:**

- Clear token
- Disable main window widgets
- Show login dialog again

## CSV Upload Interface

### Upload Widget

**Layout:** QVBoxLayout

**Elements:**

- QLabel: "Select CSV File"
- QPushButton: "Browse..." to open file dialog
- QLabel: Display selected filename
- QPushButton: "Upload" to send file
- QProgressBar or QLabel: Upload status

### File Selection

**File Dialog:**

```python
from PyQt5.QtWidgets import QFileDialog

filepath, _ = QFileDialog.getOpenFileName(
    self,
    "Select CSV File",
    "",
    "CSV Files (*.csv)"
)
```

**After Selection:**

- Store filepath in instance variable
- Display filename in label
- Enable upload button

### Upload Process

**Step 1:** Read file content

```python
with open(filepath, 'rb') as f:
    file_content = f.read()
```

**Step 2:** Prepare multipart request

```python
files = {'file': (os.path.basename(filepath), file_content, 'text/csv')}
headers = {'Authorization': f'Token {self.auth_token}'}
```

**Step 3:** Send POST request

```python
response = requests.post(
    'http://localhost:8000/api/upload/',
    files=files,
    headers=headers
)
```

**Step 4:** Handle response

**Success (201):**

```python
data = response.json()
self.display_summary(data)
self.display_charts(data)
self.refresh_history()
```

**Error (400, 401, 413):**

```python
error_msg = response.json().get('error', 'Upload failed')
QMessageBox.critical(self, "Upload Error", error_msg)
```

### Upload Feedback

**During Upload:**

- Disable upload button
- Show progress indicator or "Uploading..." status
- Optionally use QProgressDialog for large files

**On Success:**

- Show success message: QMessageBox.information()
- Update UI with new data
- Re-enable upload button

**On Error:**

- Show error dialog with message
- Re-enable upload button

## Data Display

### Summary Statistics Widget

**Layout:** QFormLayout or QGridLayout

**Elements:** QLabel pairs for each statistic

**Content:**

- Filename: [value]
- Upload Date: [formatted timestamp]
- Total Count: [value]
- Average Flowrate: [value]
- Average Pressure: [value]
- Average Temperature: [value]

**Update Method:**

```python
def display_summary(self, data):
    self.filename_label.setText(data['filename'])
    self.upload_date_label.setText(data['uploaded_at'])
    self.total_count_label.setText(str(data['total_count']))
    self.avg_flowrate_label.setText(f"{data['avg_flowrate']:.2f}")
    self.avg_pressure_label.setText(f"{data['avg_pressure']:.2f}")
    self.avg_temperature_label.setText(f"{data['avg_temperature']:.2f}")
```

## Chart Visualization

### Matplotlib Integration

**Import:**

```python
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
```

**Create Canvas:**

```python
self.figure = Figure(figsize=(8, 6))
self.canvas = FigureCanvas(self.figure)
layout.addWidget(self.canvas)
```

### Chart 1: Type Distribution

**Chart Type:** Bar chart or Pie chart

**Data Source:** `type_distribution` from response

**Implementation:**

```python
def plot_type_distribution(self, type_dist):
    self.figure.clear()
    ax = self.figure.add_subplot(111)
    
    types = list(type_dist.keys())
    counts = list(type_dist.values())
    
    ax.bar(types, counts)
    ax.set_xlabel('Equipment Type')
    ax.set_ylabel('Count')
    ax.set_title('Equipment Type Distribution')
    
    self.canvas.draw()
```

**Alternative (Pie Chart):**

```python
ax.pie(counts, labels=types, autopct='%1.1f%%')
ax.set_title('Equipment Type Distribution')
```

### Chart 2: Average Values

**Chart Type:** Bar chart

**Data:** Average flowrate, pressure, temperature

**Implementation:**

```python
def plot_averages(self, avg_flowrate, avg_pressure, avg_temp):
    self.figure.clear()
    ax = self.figure.add_subplot(111)
    
    parameters = ['Flowrate', 'Pressure', 'Temperature']
    values = [avg_flowrate, avg_pressure, avg_temp]
    
    ax.bar(parameters, values)
    ax.set_xlabel('Parameter')
    ax.set_ylabel('Average Value')
    ax.set_title('Average Parameter Values')
    
    self.canvas.draw()
```

### Multiple Charts Layout

**Option 1:** Multiple canvases in layout

**Option 2:** Subplots in single figure

```python
self.figure.clear()
ax1 = self.figure.add_subplot(121)
ax2 = self.figure.add_subplot(122)

# Plot type distribution on ax1
# Plot averages on ax2

self.figure.tight_layout()
self.canvas.draw()
```

## History Display

### History Widget

**Type:** QTableWidget or QListWidget

**Columns (Table):**

- ID
- Filename
- Upload Date
- Total Count

**Data Source:** GET `/api/history/`

### History Retrieval

```python
def load_history(self):
    response = requests.get(
        'http://localhost:8000/api/history/',
        headers={'Authorization': f'Token {self.auth_token}'}
    )
    
    if response.status_code == 200:
        history_data = response.json()
        self.populate_history_table(history_data)
    else:
        QMessageBox.warning(self, "Error", "Failed to load history")
```

### Table Population

```python
def populate_history_table(self, history):
    self.history_table.setRowCount(len(history))
    
    for row, dataset in enumerate(history):
        self.history_table.setItem(row, 0, QTableWidgetItem(str(dataset['id'])))
        self.history_table.setItem(row, 1, QTableWidgetItem(dataset['filename']))
        self.history_table.setItem(row, 2, QTableWidgetItem(dataset['uploaded_at']))
        self.history_table.setItem(row, 3, QTableWidgetItem(str(dataset['total_count'])))
```

### History Interaction

**Row Selection:**

- User clicks on row to select dataset
- Enable "View Details" and "Generate Report" buttons

**Double-Click:**

- Load dataset details and charts for selected dataset

## PDF Report Generation

### Report Request

**Trigger:** User clicks "Generate Report" button with dataset selected

**Request:**

```python
def generate_report(self, dataset_id):
    response = requests.get(
        f'http://localhost:8000/api/report/{dataset_id}/',
        headers={'Authorization': f'Token {self.auth_token}'}
    )
    
    if response.status_code == 200:
        self.save_pdf(response.content, dataset_id)
    else:
        error = response.json().get('error', 'Failed to generate report')
        QMessageBox.critical(self, "Error", error)
```

### Save PDF Dialog

```python
def save_pdf(self, pdf_content, dataset_id):
    filepath, _ = QFileDialog.getSaveFileName(
        self,
        "Save PDF Report",
        f"report_{dataset_id}.pdf",
        "PDF Files (*.pdf)"
    )
    
    if filepath:
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        QMessageBox.information(self, "Success", "Report saved successfully")
```

### Report Generation Feedback

**During Generation:**

- Show QProgressDialog or status message
- Disable button temporarily

**On Success:**

- Open save dialog
- Confirm save with message box

**On Error:**

- Display error message
- Re-enable button

## Error Handling

### Network Errors

**Exception:** requests.exceptions.RequestException

**Handling:**

```python
try:
    response = requests.get(url, headers=headers)
except requests.exceptions.RequestException as e:
    QMessageBox.critical(self, "Network Error", "Cannot connect to server")
```

### HTTP Errors

**400 Bad Request:**

```python
if response.status_code == 400:
    error_msg = response.json().get('error')
    QMessageBox.warning(self, "Validation Error", error_msg)
```

**401 Unauthorized:**

```python
if response.status_code == 401:
    self.auth_token = None
    self.show_login_dialog()
```

**404 Not Found:**

```python
if response.status_code == 404:
    QMessageBox.information(self, "Not Found", "Dataset not found")
```

**500 Server Error:**

```python
if response.status_code == 500:
    QMessageBox.critical(self, "Server Error", "Server encountered an error")
```

### JSON Parsing Errors

**Exception:** json.JSONDecodeError or ValueError

**Handling:**

```python
try:
    data = response.json()
except ValueError:
    QMessageBox.critical(self, "Error", "Invalid response from server")
```

## Threading for Network Operations

### Background Thread for Long Operations

**Purpose:** Prevent UI freezing during network requests

**Implementation:** QThread

```python
from PyQt5.QtCore import QThread, pyqtSignal

class UploadThread(QThread):
    upload_complete = pyqtSignal(dict)
    upload_error = pyqtSignal(str)
    
    def __init__(self, filepath, token):
        super().__init__()
        self.filepath = filepath
        self.token = token
    
    def run(self):
        try:
            with open(self.filepath, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(
                    'http://localhost:8000/api/upload/',
                    files=files,
                    headers=headers
                )
            
            if response.status_code == 201:
                self.upload_complete.emit(response.json())
            else:
                error = response.json().get('error', 'Upload failed')
                self.upload_error.emit(error)
        except Exception as e:
            self.upload_error.emit(str(e))
```

**Usage:**

```python
self.upload_thread = UploadThread(filepath, self.auth_token)
self.upload_thread.upload_complete.connect(self.on_upload_success)
self.upload_thread.upload_error.connect(self.on_upload_error)
self.upload_thread.start()
```

**Note:** Threading optional for simplicity, but recommended for better UX

## Menu Bar

### File Menu

**Actions:**

- Open CSV (trigger file dialog and upload)
- Exit (close application)

**Implementation:**

```python
menubar = self.menuBar()
file_menu = menubar.addMenu('File')

open_action = file_menu.addAction('Open CSV')
open_action.triggered.connect(self.open_csv_file)

exit_action = file_menu.addAction('Exit')
exit_action.triggered.connect(self.close)
```

### View Menu (Optional)

**Actions:**

- History (show history widget)
- Charts (show charts widget)

## Layout Organization

### Tab Widget Approach

**Use QTabWidget** to organize different sections:

**Tab 1:** Upload and Summary

**Tab 2:** Charts

**Tab 3:** History

**Implementation:**

```python
self.tabs = QTabWidget()
self.tabs.addTab(self.upload_widget, "Upload")
self.tabs.addTab(self.charts_widget, "Charts")
self.tabs.addTab(self.history_widget, "History")
self.setCentralWidget(self.tabs)
```

### Single Window Approach

**Use QSplitter** to divide main window:

**Left Panel:** Upload and history

**Right Panel:** Summary and charts

## UI Styling

### Default Style

**Acceptable:** Use default PyQt5 styling

**Platform Native:** Automatically uses OS native look and feel

### Custom Styling (Optional)

**Method:** QSS (Qt Style Sheets)

**Example:**

```python
self.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
```

## Window Close Behavior

### Confirmation on Exit (Optional)

**Implementation:**

```python
def closeEvent(self, event):
    reply = QMessageBox.question(
        self,
        'Exit',
        'Are you sure you want to exit?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()
```

## Configuration

### Backend URL Configuration

**Hardcoded:** `http://localhost:8000`

**Alternative:** Use configuration file or settings dialog

**Config File Approach:**

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
base_url = config.get('API', 'base_url', fallback='http://localhost:8000')
```

## Dependencies

### Required Python Packages

- PyQt5
- matplotlib
- requests

**Installation:**

```bash
pip install PyQt5 matplotlib requests
```

### Requirements File

**requirements.txt:**

```
PyQt5>=5.15.0
matplotlib>=3.3.0
requests>=2.25.0
```

## Application Packaging (Optional)

**Not Required:** Task does not require executable distribution

**If Desired:** Use PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Testing

### Manual Testing Steps

1. Launch application
2. Enter credentials and login
3. Select sample_equipment_data.csv file (or any valid CSV with 5 required columns)
4. Upload and verify summary display shows:
   - total_count matching actual row count in CSV
   - Computed averages with 2 decimal places
   - Type distribution reflecting actual type frequencies in data
5. Verify charts render correctly with data-driven labels and values
6. Check history shows uploaded dataset
7. Generate PDF report and save
8. Test error scenarios (invalid CSV, wrong credentials)

## Error Messages

### User-Friendly Messages

**Network Error:** "Cannot connect to server. Please ensure the backend is running."

**Invalid Credentials:** "Invalid username or password."

**File Error:** "Failed to read file. Please ensure it is a valid CSV."

**Upload Error:** Display specific error from backend response
