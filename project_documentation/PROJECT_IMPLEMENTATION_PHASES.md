# FOSSEE Internship 2026 - Project Implementation Phases

## Overview

This document defines the complete implementation plan for the Chemical Equipment Parameter Visualizer hybrid application. Each phase is independent, testable, and must be completed before proceeding to the next.

---

## Phase 1: Django Project Initialization and Database Setup

### Purpose
Establish the backend foundation with Django, configure the database, and create the core data model.

### Components Implemented
- Django project structure
- Django app for API
- EquipmentDataset model
- SQLite database configuration
- Initial migrations

### Completion Criteria
- Django server starts without errors
- Database migrations apply successfully
- EquipmentDataset table exists in SQLite
- Model has all required fields: id, uploaded_at, filename, total_count, avg_flowrate, avg_pressure, avg_temperature, type_distribution, csv_data
- Can create and save EquipmentDataset records via Django shell

### NOT Implemented Yet
- API endpoints
- Authentication
- CSV processing logic
- Frontend applications
- PDF generation

### Validation
- Run `python manage.py runserver` successfully
- Run `python manage.py migrate` without errors
- Create sample record in Django shell and verify it saves

---

## Phase 2: Django REST Framework and Authentication Setup

### Purpose
Configure Django REST Framework and implement token-based authentication system.

### Components Implemented
- Django REST Framework configuration
- rest_framework.authtoken app
- Token model migration
- Login endpoint for token generation
- Test user creation

### Completion Criteria
- DRF installed and configured
- Token table exists in database
- Login endpoint at `/api/login/` responds to POST requests
- Valid credentials return token in JSON response
- Invalid credentials return 401 error
- Test user exists for authentication testing

### NOT Implemented Yet
- CSV upload endpoint
- Protected endpoints
- Data processing logic
- Frontend applications
- History management
- PDF generation

### Validation
- POST to `/api/login/` with valid credentials returns token
- POST with invalid credentials returns 401
- Token persists in database after generation

---

## Phase 3: CSV Upload Endpoint (Basic)

### Purpose
Implement the CSV file upload endpoint with basic file reception and storage.

### Components Implemented
- Upload API view at `/api/upload/`
- File reception from multipart/form-data
- Basic file validation (extension, existence)
- Authentication requirement on upload endpoint
- Minimal response structure

### Completion Criteria
- Upload endpoint accepts authenticated POST requests with file
- Endpoint requires valid authentication token
- Returns 401 if token missing or invalid
- Returns 400 if file missing
- Returns 400 if file is not CSV
- Returns 201 with basic response for valid CSV file

### NOT Implemented Yet
- CSV parsing with Pandas
- Analytics computation
- Database storage of dataset
- History management
- Visualization endpoints
- PDF generation
- Frontend applications

### Validation
- POST CSV file with valid token returns 201
- POST without token returns 401
- POST non-CSV file returns 400
- POST without file returns 400

---

## Phase 4: CSV Parsing and Validation

### Purpose
Implement Pandas-based CSV parsing with complete validation logic.

### Components Implemented
- Pandas CSV reading
- Column validation (exact names required)
- Data type conversion for numeric columns
- Row validation and cleaning
- Detailed error messages for validation failures

### Completion Criteria
- CSV is parsed into Pandas DataFrame
- Missing columns return 400 with specific column names listed
- Invalid numeric values return 400 with row and column identified
- Empty CSV returns 400
- Valid CSV passes all validation checks
- Cleaned DataFrame has no NaN values

### NOT Implemented Yet
- Analytics computation
- Database storage
- History management
- Other endpoints
- PDF generation
- Frontend applications

### Validation
- Upload CSV with missing column returns specific error
- Upload CSV with invalid numeric value returns row/column error
- Upload valid sample_equipment_data.csv passes validation
- Upload empty CSV returns error

---

## Phase 5: Analytics Computation

### Purpose
Implement all required analytics computations using Pandas.

### Components Implemented
- Total count computation
- Average flowrate computation (rounded to 2 decimals)
- Average pressure computation (rounded to 2 decimals)
- Average temperature computation (rounded to 2 decimals)
- Type distribution computation

### Completion Criteria
- All five analytics are computed correctly from DataFrame
- Averages rounded to exactly 2 decimal places
- Type distribution is dictionary with type names as keys
- Type distribution counts sum to total count
- Computation works for any valid CSV dataset

### NOT Implemented Yet
- Database storage of analytics
- History management
- Response formatting with analytics
- Other endpoints
- PDF generation
- Frontend applications

### Validation
- Upload sample CSV and verify computed values are correct
- Verify averages have exactly 2 decimal places
- Verify type distribution sums equal total count
- Test with different CSV files to ensure generic computation

---

## Phase 6: Database Storage and Response Formatting

### Purpose
Save computed analytics to database and return complete JSON response.

### Components Implemented
- EquipmentDataset record creation with all fields
- CSV content storage as text
- Complete upload response JSON structure
- Serializer for EquipmentDataset model

### Completion Criteria
- Uploaded dataset saves to database with all analytics
- Response includes id, filename, uploaded_at, total_count, averages, type_distribution
- Timestamp is ISO 8601 format
- CSV content stored in csv_data field
- Each upload creates one database record

### NOT Implemented Yet
- History constraint (last 5 only)
- History endpoint
- Dataset detail endpoint
- Visualization endpoint
- PDF generation
- Frontend applications

### Validation
- Upload CSV and verify database record exists
- Verify response JSON has all required fields
- Query database and confirm all analytics stored correctly
- Upload multiple CSVs and verify each creates separate record

---

## Phase 7: History Management (Last 5 Constraint)

### Purpose
Implement automatic deletion of oldest datasets to maintain exactly last 5 uploads.

### Components Implemented
- History constraint enforcement after each upload
- Deletion logic for datasets beyond 5th
- Transaction handling for atomic operations

### Completion Criteria
- After 5 uploads, database contains 5 datasets
- After 6th upload, oldest dataset is deleted automatically
- After 10th upload, database still contains only 5 most recent
- Deletion happens within same transaction as upload
- Most recent 5 datasets are always retained

### NOT Implemented Yet
- History retrieval endpoint
- Dataset detail endpoint
- Visualization endpoint
- PDF generation
- Frontend applications

### Validation
- Upload 5 CSVs, verify database has 5 records
- Upload 6th CSV, verify oldest is deleted and count remains 5
- Upload 10 CSVs, verify only last 5 remain
- Check that IDs of remaining datasets are correct

---

## Phase 8: History Endpoint

### Purpose
Implement endpoint to retrieve list of last 5 uploaded datasets.

### Components Implemented
- History API view at `/api/history/`
- Query for last 5 datasets ordered by upload time
- Authentication requirement
- JSON array response with dataset summaries

### Completion Criteria
- GET request to `/api/history/` returns array of datasets
- Requires authentication token
- Returns 401 if token missing or invalid
- Datasets ordered by uploaded_at descending (most recent first)
- Maximum 5 datasets in response
- Each dataset includes all summary fields

### NOT Implemented Yet
- Dataset detail endpoint
- Visualization endpoint
- PDF generation
- Frontend applications

### Validation
- Upload 3 datasets, GET history returns 3 in correct order
- Upload 7 datasets, GET history returns only 5 most recent
- Verify most recent upload appears first in array
- Request without token returns 401

---

## Phase 9: Dataset Detail and Visualization Endpoints

### Purpose
Implement endpoints for retrieving specific dataset details and visualization-formatted data.

### Components Implemented
- Dataset detail endpoint at `/api/dataset/<id>/`
- Visualization data endpoint at `/api/dataset/<id>/visualization/`
- Authentication requirements
- Proper error handling for non-existent datasets

### Completion Criteria
- GET `/api/dataset/<id>/` returns full dataset details
- GET `/api/dataset/<id>/visualization/` returns chart-formatted data
- Both endpoints require authentication
- Both return 404 if dataset ID not found
- Visualization endpoint formats type_distribution and averages for charting

### NOT Implemented Yet
- PDF generation
- Frontend applications

### Validation
- Request existing dataset returns correct data
- Request non-existent dataset returns 404
- Request without token returns 401
- Visualization endpoint returns properly formatted labels and data arrays

---

## Phase 10: PDF Report Generation

### Purpose
Implement PDF report generation using ReportLab.

### Components Implemented
- PDF generation utility function
- Report endpoint at `/api/report/<id>/`
- PDF content: title, dataset info, summary statistics, type distribution table
- File response with correct headers

### Completion Criteria
- GET `/api/report/<id>/` generates and returns PDF
- PDF contains all required sections
- Response headers set Content-Type and Content-Disposition correctly
- Returns 404 if dataset not found
- Returns 401 if not authenticated
- PDF file downloads correctly with filename `report_<id>.pdf`

### NOT Implemented Yet
- Frontend applications

### Validation
- Request report for existing dataset downloads PDF
- Open PDF and verify all sections present
- Verify statistics in PDF match database values
- Request for non-existent dataset returns 404

---

## Phase 11: Backend Integration Testing

### Purpose
Comprehensive testing of all backend endpoints together.

### Components Implemented
- Complete backend API testing
- Multi-upload workflow testing
- Error scenario testing

### Completion Criteria
- Can authenticate and receive token
- Can upload multiple CSVs successfully
- History maintains last 5 constraint correctly
- All endpoints respond correctly
- Error cases handled properly
- No data corruption or race conditions

### NOT Implemented Yet
- Frontend applications

### Validation
- Execute complete workflow: login → upload 10 files → check history → generate PDFs
- Verify data consistency across all endpoints
- Test concurrent uploads if time permits
- Document any issues found and resolved

---

## Phase 12: React Project Initialization

### Purpose
Set up React application structure and development environment.

### Components Implemented
- React project using Create React App or Vite
- Project folder structure
- Component file stubs
- Development server configuration
- Chart.js installation

### Completion Criteria
- React development server starts
- Can access app at http://localhost:3000
- Basic component structure in place
- Chart.js and dependencies installed
- No build errors

### NOT Implemented Yet
- Authentication UI
- Upload functionality
- Charts
- History display
- Backend integration
- Desktop application

### Validation
- Run `npm start` successfully
- Open browser and see React app
- Verify Chart.js in package.json

---

## Phase 13: React Authentication Implementation

### Purpose
Implement login interface and token management in React.

### Components Implemented
- Login component with form
- Token storage in localStorage
- API service for login request
- Authentication state management
- Protected route logic

### Completion Criteria
- Login form accepts username and password
- Successful login stores token
- Failed login shows error message
- Token persists across page reloads
- Can detect authentication state on app load
- Authenticated state unlocks main interface

### NOT Implemented Yet
- CSV upload UI
- Data visualization
- History display
- PDF download
- Desktop application

### Validation
- Enter valid credentials and verify token stored
- Reload page and verify still authenticated
- Enter invalid credentials and see error
- Clear localStorage and verify requires login again

---

## Phase 14: React CSV Upload Interface

### Purpose
Implement file upload functionality in React.

### Components Implemented
- Upload component with file input
- FormData construction
- Upload request to backend with authentication
- Loading state during upload
- Success and error handling

### Completion Criteria
- Can select CSV file using file input
- Upload button sends file to backend
- Loading indicator shows during upload
- Success displays summary statistics
- Errors display backend error messages
- Token included in Authorization header

### NOT Implemented Yet
- Data visualization
- History display
- PDF download
- Desktop application

### Validation
- Upload sample CSV and verify success response
- Verify summary statistics display
- Upload invalid CSV and see error message
- Verify network request includes authentication token

---

## Phase 15: React Chart Visualization

### Purpose
Implement Chart.js visualizations for type distribution and averages.

### Components Implemented
- Charts component
- Type distribution chart (bar or pie)
- Averages chart (bar)
- Data fetching from visualization endpoint
- Chart rendering with Chart.js

### Completion Criteria
- Charts display after successful upload
- Type distribution chart shows all equipment types
- Averages chart shows three parameters
- Charts update when new dataset uploaded
- Charts are responsive and readable

### NOT Implemented Yet
- History display
- PDF download
- Desktop application

### Validation
- Upload CSV and verify both charts render
- Verify chart data matches backend response
- Upload different CSV and verify charts update
- Resize window and verify charts remain readable

---

## Phase 16: React History and PDF Features

### Purpose
Implement dataset history list and PDF report download.

### Components Implemented
- History component with dataset list
- History API call
- PDF download functionality
- User interaction for selecting datasets

### Completion Criteria
- History list displays last 5 datasets
- Most recent dataset appears first
- Can trigger PDF download for any dataset
- PDF downloads with correct filename
- History refreshes after new upload

### NOT Implemented Yet
- Desktop application

### Validation
- Upload multiple datasets and verify history updates
- Click download PDF and verify file saves
- Upload 6th dataset and verify oldest removed from history
- Verify history shows correct timestamps

---

## Phase 17: React Integration and Polish

### Purpose
Complete React application with full workflow integration and UI polish.

### Components Implemented
- Full application workflow
- Navigation between sections
- Error boundary components
- Loading states
- User feedback messages

### Completion Criteria
- Complete workflow works: login → upload → view charts → check history → download PDF
- All user actions have appropriate feedback
- No console errors
- Clean, readable interface
- Responsive design basics

### NOT Implemented Yet
- Desktop application

### Validation
- Execute complete user workflow multiple times
- Test all error scenarios
- Verify all features work together
- Check browser console for errors

---

## Phase 18: PyQt5 Project Initialization

### Purpose
Set up PyQt5 desktop application structure.

### Components Implemented
- Main application entry point
- Main window class
- Basic window layout
- Menu structure
- Component file stubs

### Completion Criteria
- Application launches and displays window
- Window has appropriate title and size
- Menu bar present
- No errors on startup
- Can close application cleanly

### NOT Implemented Yet
- Login dialog
- Upload functionality
- Charts
- History
- Backend integration

### Validation
- Run `python main.py` and verify window appears
- Verify window title is correct
- Test menu items (even if non-functional)
- Close window and verify clean exit

---

## Phase 19: PyQt5 Authentication Dialog

### Purpose
Implement login dialog for desktop application.

### Components Implemented
- Login dialog with username and password fields
- API request for authentication
- Token storage in memory or QSettings
- Dialog acceptance on success
- Error message display

### Completion Criteria
- Login dialog appears on application start
- Valid credentials store token and close dialog
- Invalid credentials show error message
- Main window remains disabled until authenticated
- Token available for subsequent requests

### NOT Implemented Yet
- Upload functionality
- Charts
- History
- PDF generation

### Validation
- Launch app and see login dialog
- Enter valid credentials and verify main window becomes accessible
- Enter invalid credentials and see error
- Verify token stored correctly

---

## Phase 20: PyQt5 CSV Upload Widget

### Purpose
Implement file selection and upload functionality in PyQt5.

### Components Implemented
- Upload widget with file selection button
- File dialog for CSV selection
- Upload request to backend
- Progress indication during upload
- Summary statistics display

### Completion Criteria
- Can open file dialog and select CSV
- Selected filename displays in UI
- Upload button sends file to backend with authentication
- Success displays summary statistics
- Errors show in message box
- Loading state during upload

### NOT Implemented Yet
- Charts display
- History widget
- PDF save functionality

### Validation
- Select sample CSV and upload successfully
- Verify summary statistics display correctly
- Upload invalid CSV and see error dialog
- Verify authentication token included in request

---

## Phase 21: PyQt5 Matplotlib Charts

### Purpose
Implement chart visualization using Matplotlib embedded in PyQt5.

### Components Implemented
- Matplotlib canvas widget
- Type distribution chart
- Averages chart
- Chart update logic after upload
- Multiple chart layout

### Completion Criteria
- Charts display after successful upload
- Type distribution chart shows all types
- Averages chart shows three parameters
- Charts embedded properly in Qt window
- Charts clear and render new data on subsequent uploads

### NOT Implemented Yet
- History widget
- PDF save functionality

### Validation
- Upload CSV and verify both charts render
- Verify chart data matches backend values
- Upload different CSV and verify charts update
- Resize window and verify charts remain visible

---

## Phase 22: PyQt5 History and PDF Features

### Purpose
Implement dataset history table/list and PDF save functionality.

### Components Implemented
- History widget (table or list)
- History API call
- PDF generation request
- File save dialog for PDF
- Dataset selection interaction

### Completion Criteria
- History widget shows last 5 datasets
- Most recent appears first
- Can select dataset from history
- Can generate and save PDF for selected dataset
- Save dialog with suggested filename

### NOT Implemented Yet
- None (desktop app feature complete)

### Validation
- Upload datasets and verify history populates
- Select dataset and generate PDF
- Save PDF and verify file created with correct content
- Upload 6th dataset and verify oldest removed

---

## Phase 23: PyQt5 Integration and Polish

### Purpose
Complete desktop application with full workflow integration.

### Components Implemented
- Full application workflow
- Tab or panel organization
- Threading for network operations (optional but recommended)
- Error handling improvements
- User experience polish

### Completion Criteria
- Complete workflow works: login → upload → view charts → check history → save PDF
- UI is organized and intuitive
- No crashes or hangs during operations
- All features functional
- Clean error messages

### NOT Implemented Yet
- None (all features complete)

### Validation
- Execute complete workflow multiple times
- Test all error scenarios
- Verify no UI freezing during uploads or PDF generation
- Test on target platform (Windows/Linux/Mac)

---

## Phase 24: Sample Data and Documentation

### Purpose
Prepare sample CSV file and complete README documentation.

### Components Implemented
- sample_equipment_data.csv file
- Comprehensive README.md
- Setup instructions for all three components
- API documentation section
- Usage instructions

### Completion Criteria
- Sample CSV file with 15 rows, 5 columns in repository
- README includes complete setup steps for backend
- README includes complete setup steps for web frontend
- README includes complete setup steps for desktop frontend
- README includes basic API endpoint reference
- README includes usage instructions

### NOT Implemented Yet
- Demo video

### Validation
- Follow README instructions on clean system to verify completeness
- Verify sample CSV has correct structure
- Test all documented commands work
- Have peer review README for clarity

---

## Phase 25: Repository Organization and Git Cleanup

### Purpose
Organize repository structure and clean up git history.

### Components Implemented
- Proper directory structure
- .gitignore files
- Clean commit history
- Meaningful commit messages

### Completion Criteria
- Repository has clean three-directory structure (backend/, web/, desktop/)
- .gitignore prevents committing unnecessary files
- No __pycache__, node_modules, db.sqlite3 in repository
- Commits are logical and well-messaged
- No sensitive data in history

### NOT Implemented Yet
- Demo video

### Validation
- Clone repository fresh and verify structure
- Check for unwanted files in git
- Review commit history for clarity
- Verify .gitignore effectiveness

---

## Phase 26: Demo Video Production

### Purpose
Create 2-3 minute demonstration video of complete application.

### Components Implemented
- Screen recording of complete workflow
- Both web and desktop applications demonstrated
- Clear narration or captions
- Video file in appropriate format

### Completion Criteria
- Video is 2-3 minutes long
- Shows backend running
- Demonstrates web app login, upload, charts, history, PDF
- Demonstrates desktop app login, upload, charts, history, PDF
- Video quality is clear and professional
- Audio (if used) is clear
- File size reasonable for sharing

### NOT Implemented Yet
- None (project complete)

### Validation
- Watch video and verify all features shown
- Verify video length meets requirement
- Test video plays on different devices
- Get feedback on clarity and completeness

---

## Phase 27: Final Testing and Validation

### Purpose
Comprehensive end-to-end testing of entire system.

### Components Implemented
- Complete integration testing
- Cross-component validation
- Edge case testing
- Performance verification

### Completion Criteria
- All six required features work correctly
- Web and desktop frontends behave identically
- History constraint (last 5) functions correctly
- PDF reports generate with correct data
- Authentication protects all endpoints
- No critical bugs remain
- Sample data works correctly
- System handles various CSV files properly

### NOT Implemented Yet
- None (project complete)

### Validation
- Test complete workflow 5+ times
- Upload 10+ different CSV files
- Test all error scenarios
- Verify data consistency across components
- Check authentication on all protected endpoints
- Generate multiple PDF reports

---

## Phase 28: Submission Preparation

### Purpose
Prepare all materials for final submission.

### Components Implemented
- GitHub repository finalization
- README verification
- Demo video upload
- Submission form preparation

### Completion Criteria
- GitHub repository is public and accessible
- Repository URL is correct and shareable
- README is complete and accurate
- Demo video is uploaded and accessible
- All submission form fields prepared
- Project meets all requirements

### NOT Implemented Yet
- None (ready for submission)

### Validation
- Access repository from incognito/different account
- Verify all files present and correct
- Watch demo video from shared link
- Review submission form requirements
- Double-check all URLs and links work

---

## Phase 29: Submission

### Purpose
Submit project via Google Form.

### Components Implemented
- Form submission with all required details

### Completion Criteria
- Google form submitted successfully
- Confirmation received
- All links verified working
- Submission timestamp before deadline

### Validation
- Receive form submission confirmation
- Access all submitted links to verify they work
- Keep confirmation for records

---

## Implementation Notes

### Phase Dependencies
- Phases 1-11: Backend (sequential)
- Phases 12-17: Web Frontend (sequential, requires completed backend)
- Phases 18-23: Desktop Frontend (sequential, requires completed backend)
- Phases 24-29: Documentation and Submission (requires all features complete)

### Critical Success Factors
- Do not skip phases
- Complete each phase fully before moving to next
- Test thoroughly at each phase completion
- Keep commits small and focused per phase
- Document issues encountered during each phase

### Time Estimates
Each phase estimated at 2-4 hours for experienced developer, adjust based on skill level.

Total estimated time: 60-100 hours for complete implementation.

### Quality Gates
After each phase, verify:
- No errors in console/terminal
- All acceptance criteria met
- Code follows style guidelines (no comments)
- Changes committed to git with clear message
- Documentation updated if needed

### Risk Mitigation
- If stuck on a phase beyond reasonable time, document blocker and seek help
- Do not proceed to next phase with known bugs in current phase
- Test incrementally; don't wait until end to test
- Keep backup commits in case of major issues

---

## Completion Checklist

After Phase 29, verify entire project:

- [ ] Django backend runs and serves API
- [ ] All API endpoints functional and authenticated
- [ ] CSV upload, parsing, and analytics work correctly
- [ ] History maintains last 5 datasets
- [ ] PDF reports generate correctly
- [ ] React web app fully functional
- [ ] PyQt5 desktop app fully functional
- [ ] Both frontends connect to same backend
- [ ] Charts display in both frontends
- [ ] Sample CSV included in repository
- [ ] README has complete setup instructions
- [ ] Demo video shows all features
- [ ] Repository is clean and organized
- [ ] Project submitted via Google Form
- [ ] All links in submission work correctly

If all items checked, project is complete and ready for evaluation.
