# FOSSEE Internship Project - Complete Implementation Guide

## Document Purpose

This document provides the complete implementation roadmap for the Chemical Equipment Parameter Visualizer hybrid application. Use this alongside the 11 detailed specification documents.

## Specification Documents Reference

1. **01_SYSTEM_BEHAVIOR_WORKFLOW.md** - Overall system architecture and end-to-end workflows
2. **02_BACKEND_RESPONSIBILITIES.md** - Backend data processing and storage logic
3. **03_API_CONTRACTS.md** - Complete API endpoint specifications
4. **04_ANALYTICS_COMPUTATIONS.md** - Exact formulas and computation rules
5. **05_HISTORY_MANAGEMENT.md** - Dataset history constraint (last 5 only)
6. **06_AUTHENTICATION.md** - Token-based authentication implementation
7. **07_PDF_GENERATION.md** - PDF report generation specifications
8. **08_WEB_FRONTEND.md** - React.js web application rules
9. **09_DESKTOP_FRONTEND.md** - PyQt5 desktop application rules
10. **10_CODING_AGENT_RULES.md** - Code quality and style constraints
11. **11_MODEL_OUTPUT_RULES.md** - Natural human-written code requirements

## Implementation Order

### Phase 1: Backend Foundation

**Step 1.1:** Django Project Setup

- Create Django project named `config`
- Create Django app named `api`
- Configure SQLite database
- Install Django REST Framework
- Install rest_framework.authtoken

**Step 1.2:** Database Models

- Implement EquipmentDataset model per 02_BACKEND_RESPONSIBILITIES.md
- Run migrations

**Step 1.3:** Authentication

- Implement login endpoint per 06_AUTHENTICATION.md
- Configure TokenAuthentication
- Create test user

**Step 1.4:** CSV Upload Endpoint

- Implement file upload view per 03_API_CONTRACTS.md
- Add Pandas CSV parsing per 02_BACKEND_RESPONSIBILITIES.md
- Implement analytics computation per 04_ANALYTICS_COMPUTATIONS.md
- Implement history management per 05_HISTORY_MANAGEMENT.md

**Step 1.5:** Additional Endpoints

- Implement history endpoint
- Implement dataset detail endpoint
- Implement visualization data endpoint
- Implement PDF report endpoint per 07_PDF_GENERATION.md

**Step 1.6:** Testing

- Test all endpoints with Postman or curl
- Verify authentication works
- Verify CSV upload and analytics
- Verify history constraint (last 5)
- Test PDF generation

### Phase 2: Web Frontend

**Step 2.1:** React Project Setup

- Create React app using Create React App or Vite
- Install Chart.js and react-chartjs-2
- Set up project structure per 08_WEB_FRONTEND.md

**Step 2.2:** Authentication UI

- Implement login component
- Implement token storage
- Implement authenticated request wrapper

**Step 2.3:** Upload Interface

- Implement file upload component
- Implement summary display
- Handle upload errors

**Step 2.4:** Visualization

- Implement Chart.js charts for type distribution
- Implement Chart.js charts for averages
- Display charts after upload

**Step 2.5:** History and Reports

- Implement history list component
- Implement PDF report download

**Step 2.6:** Integration Testing

- Test complete workflow: login → upload → view charts → history → PDF
- Test error scenarios
- Verify responsive behavior

### Phase 3: Desktop Frontend

**Step 3.1:** PyQt5 Project Setup

- Create main application file
- Set up project structure per 09_DESKTOP_FRONTEND.md
- Create requirements.txt with PyQt5, matplotlib, requests

**Step 3.2:** Authentication Dialog

- Implement login dialog
- Implement token storage

**Step 3.3:** Main Window

- Implement main window layout
- Create upload widget
- Create summary display widget

**Step 3.4:** Charts

- Implement Matplotlib chart widget
- Embed charts in main window
- Display type distribution chart
- Display averages chart

**Step 3.5:** History and Reports

- Implement history list/table widget
- Implement PDF save dialog

**Step 3.6:** Integration Testing

- Test complete workflow
- Test error handling
- Verify charts display correctly

### Phase 4: Final Integration

**Step 4.1:** Sample Data

- Create sample_equipment_data.csv per specification
- Test with sample data in both frontends

**Step 4.2:** Documentation

- Write comprehensive README.md
- Include setup instructions for all three components
- Document API endpoints briefly
- Add testing instructions

**Step 4.3:** Repository Cleanup

- Remove unnecessary files
- Configure .gitignore
- Organize directory structure
- Commit with clean history

**Step 4.4:** Demo Video

- Record 2-3 minute demo video
- Show login in both applications
- Demonstrate CSV upload
- Show charts rendering
- Display history
- Generate PDF report

**Step 4.5:** Submission

- Push to GitHub
- Ensure README is complete
- Verify all features work
- Submit via Google Form

## Critical Success Factors

### Must Have

1. All three components working (backend, web, desktop)
2. CSV upload functional in both frontends
3. Analytics computed correctly per specification
4. Charts displaying in both frontends
5. History maintaining exactly last 5 datasets
6. PDF report generation working
7. Authentication protecting all endpoints
8. Complete setup instructions in README

### Must Not Have

1. No comments in code
2. No features beyond specification
3. No AI-style code patterns
4. No bugs in core functionality

## Technology Versions

### Backend

- Python 3.8 or higher
- Django 4.0 or higher
- Django REST Framework 3.13 or higher
- Pandas 1.3 or higher
- ReportLab 3.6 or higher

### Web Frontend

- React 18 or higher
- Chart.js 3.0 or higher
- Modern browser (Chrome, Firefox, Safari, Edge)

### Desktop Frontend

- Python 3.8 or higher
- PyQt5 5.15 or higher
- Matplotlib 3.3 or higher

## File Structure Template

```
fossee-internship-project/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       └── utils.py
├── web/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── components/
│       │   ├── Login.js
│       │   ├── Upload.js
│       │   ├── Charts.js
│       │   └── History.js
│       └── services/
│           └── api.js
├── desktop/
│   ├── main.py
│   ├── requirements.txt
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── login_dialog.py
│   │   ├── upload_widget.py
│   │   ├── charts_widget.py
│   │   └── history_widget.py
│   └── services/
│       └── api_client.py
├── sample_equipment_data.csv
├── README.md
└── .gitignore
```

## Sample CSV Format Reference

The sample dataset is a reference example demonstrating valid CSV structure. The system must handle arbitrary datasets following the same schema.

**Sample Structure:** 15 rows, 5 columns (row count is not fixed)

**Required Schema (applies to all datasets):**

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
```

**Sample Content (illustrative only):**

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,120,15.2,350
Heat Exchanger B,Heat Exchanger,80,10.5,280
Pump C,Pump,150,20.0,300
Reactor D,Reactor,110,14.8,340
Heat Exchanger E,Heat Exchanger,85,11.0,285
Pump F,Pump,145,19.5,295
Reactor G,Reactor,115,15.0,345
Heat Exchanger H,Heat Exchanger,90,11.5,290
Pump I,Pump,140,19.0,305
Reactor J,Reactor,125,15.5,355
Heat Exchanger K,Heat Exchanger,88,11.2,287
Pump L,Pump,142,19.2,302
Reactor M,Reactor,118,15.1,348
Heat Exchanger N,Heat Exchanger,82,10.8,283
Pump O,Pump,148,19.8,298
```

**Column Data Types (flexible parsing):**
- Equipment Name: String (any non-empty text)
- Type: String (any non-empty text; no predefined list)
- Flowrate: Numeric (integer or float, parsed as float)
- Pressure: Numeric (integer or float, parsed as float)
- Temperature: Numeric (integer or float, parsed as float)

**Important:** System must handle datasets with different row counts, different equipment type names, different type distributions, and different numeric value ranges.

## Common Pitfalls to Avoid

### Backend

- Forgetting to enforce history limit after each upload
- Not handling CSV validation errors properly
- Missing authentication on protected endpoints
- Not rounding averages to 2 decimal places
- Storing more than 5 datasets

### Web Frontend

- Not including token in Authorization header
- Forgetting to handle 401 responses
- Not refreshing history after upload
- Hardcoding backend URL without configuration

### Desktop Frontend

- Not running network operations in background threads
- Forgetting to include token in requests
- Not handling file dialog cancellation
- Memory leaks from matplotlib figures not being cleared

## Verification Checklist

### Backend Verification

- [ ] Django server starts without errors
- [ ] Login endpoint returns token for valid credentials
- [ ] Upload endpoint accepts CSV and returns summary
- [ ] Analytics values are correct (2 decimal places for averages)
- [ ] History endpoint returns max 5 datasets
- [ ] After 6 uploads, oldest is deleted
- [ ] PDF endpoint generates and returns PDF
- [ ] All endpoints require authentication except login

### Web Frontend Verification

- [ ] Login form accepts credentials and stores token
- [ ] File upload works and displays summary
- [ ] Charts render correctly after upload
- [ ] History list shows datasets
- [ ] PDF download works
- [ ] Error messages display for failed operations
- [ ] 401 redirects to login

### Desktop Frontend Verification

- [ ] Login dialog appears on startup
- [ ] Login success closes dialog and shows main window
- [ ] File selection dialog works
- [ ] Upload displays summary statistics
- [ ] Charts display using matplotlib
- [ ] History table/list populates
- [ ] PDF save dialog works

## Testing Workflow

1. Start Django backend server
2. Create test user via Django admin or createsuperuser
3. Start React web app
4. Open desktop application
5. Login to web app with test credentials
6. Upload sample_equipment_data.csv in web app
7. Verify summary displays computed values based on actual CSV content
8. Verify charts display with data-driven type labels and counts
9. Upload 4 more CSV files (can use modified copies or different datasets)
10. Verify history shows 5 datasets
11. Upload 6th CSV
12. Verify oldest dataset is removed from history
13. Generate PDF report
14. Verify PDF contains correct computed statistics from selected dataset
15. Login to desktop app
16. Upload CSV in desktop app (sample or other valid CSV)
17. Verify summary, charts, and history display data-driven values
18. Generate and save PDF from desktop app
19. Test error scenarios (invalid CSV, wrong credentials, missing columns)
20. Test with CSV files of different sizes (e.g., 5 rows, 50 rows, 100 rows)

## Submission Preparation

### GitHub Repository

**Repository Name:** `fossee-internship-2026` or similar

**Branches:** Main branch only (or development + main)

**Commit Messages:** Clear and descriptive

### README.md Template

```markdown
# Chemical Equipment Parameter Visualizer

Hybrid Web + Desktop application for chemical equipment data visualization and analytics.

## Tech Stack

- Backend: Django + Django REST Framework
- Web Frontend: React.js + Chart.js
- Desktop Frontend: PyQt5 + Matplotlib
- Database: SQLite

## Setup Instructions

### Backend Setup

[Step-by-step instructions]

### Web Frontend Setup

[Step-by-step instructions]

### Desktop Frontend Setup

[Step-by-step instructions]

## Usage

[Instructions for using the application]

## API Documentation

[Brief API endpoint reference]

## Sample Data

Use `sample_equipment_data.csv` for testing.

## Demo Video

[Link to demo video]
```

### Demo Video Content

**Duration:** 2-3 minutes

**Content:**

1. Brief introduction (10 seconds)
2. Backend running (5 seconds)
3. Web app login and upload (30 seconds)
4. Web app charts and history (20 seconds)
5. Web app PDF generation (10 seconds)
6. Desktop app login and upload (30 seconds)
7. Desktop app charts and history (20 seconds)
8. Desktop app PDF save (10 seconds)
9. Brief conclusion (5 seconds)

**Recording Tool:** OBS Studio, Loom, or similar

**Format:** MP4 or similar web-compatible format

## Additional Notes

### Optional Features

The specification mentions "Optional: Deployment link for web version"

**If deploying web app:**

- Use Vercel, Netlify, or GitHub Pages for frontend
- Configure CORS in Django backend for production domain
- Update API URL in React app for production
- Include deployment link in README and submission

**This is optional and not required for evaluation**

### Development Tips

- Test frequently during development
- Keep code commits small and focused
- Run backend and frontends simultaneously during testing
- Use browser developer tools for debugging web app
- Use PyQt5 debugger or print statements for desktop app
- Refer to specification documents frequently

## Final Pre-Submission Check

- [ ] All code has no comments
- [ ] Code style follows natural human patterns
- [ ] All 6 required features implemented
- [ ] README has complete setup instructions
- [ ] Sample CSV file included in repository
- [ ] Demo video recorded and uploaded
- [ ] GitHub repository is public and accessible
- [ ] Submission form filled with all details

## Support Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React Documentation: https://react.dev/
- Chart.js Documentation: https://www.chartjs.org/
- PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Matplotlib Documentation: https://matplotlib.org/
- Pandas Documentation: https://pandas.pydata.org/

**Remember:** Use these for reference only. Implementation must follow project specifications strictly.
