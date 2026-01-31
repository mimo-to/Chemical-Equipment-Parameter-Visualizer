# Coding Agent Rules and Constraints

## Primary Directive

Implement the FOSSEE Semester Internship 2026 screening project exactly as specified in the official task documents and supporting specification files.

## Scope Constraints

### What Must Be Implemented

1. Django backend with Django REST Framework
2. React.js web frontend with Chart.js
3. PyQt5 desktop frontend with Matplotlib
4. CSV upload functionality in both frontends
5. Data parsing and analytics using Pandas
6. Summary statistics API endpoint
7. Visualization endpoints
8. Dataset history management (last 5 only)
9. PDF report generation
10. Token-based authentication
11. SQLite database storage

### What Must NOT Be Added

- Features not mentioned in task specification
- Additional endpoints beyond those specified
- User registration or password reset
- Advanced authentication (OAuth, JWT with refresh, MFA)
- Data export formats other than PDF
- Real-time updates or WebSockets
- User-specific data isolation (unless explicitly implementing)
- Pagination beyond the 5-item history constraint
- Advanced analytics (median, standard deviation, outliers)
- Chart types not mentioned (scatter, line, heatmap)
- Email notifications
- Scheduled tasks or background jobs
- API rate limiting (unless explicitly desired)
- Search or filtering in history
- Data validation beyond specified requirements
- Admin dashboard beyond Django's built-in admin

## Code Style Rules

### Python Code Style

**Formatting:**

- 4 spaces for indentation
- Maximum line length: 100 characters
- Use snake_case for variables and functions
- Use PascalCase for class names
- No trailing whitespace

**Imports:**

- Standard library imports first
- Third-party imports second
- Local imports third
- Alphabetical order within each group

**Functions:**

- Keep functions focused on single responsibility
- Avoid deeply nested logic (max 3 levels)
- Use descriptive names, avoid abbreviations

**Classes:**

- Group related methods together
- Use class methods and static methods appropriately
- Avoid overly large classes

### JavaScript/React Code Style

**Formatting:**

- 2 spaces for indentation
- Use const/let, never var
- Use arrow functions for callbacks
- Semicolons required

**Components:**

- Functional components only (no class components unless necessary)
- Use hooks for state and effects
- One component per file
- Component names in PascalCase

**Naming:**

- camelCase for variables and functions
- PascalCase for components
- UPPER_CASE for constants
- Descriptive names over short names

### Prohibited Patterns

**No AI-Style Verbosity:**

- No excessive variable names like `resultFromApiCallForDatasetHistory`
- Use concise names: `history`, `dataset`, `response`

**No Unnecessary Abstractions:**

- No generic "service layer" unless it simplifies code
- No design patterns applied without clear benefit
- No "future-proofing" for features not in spec

**No Over-Engineering:**

- No complex state management for simple apps
- No microservices architecture
- No unnecessary configuration files
- No premature optimization

## Comment Rules (STRICT)

### Absolute Prohibition

**NO COMMENTS IN CODE**

This includes:

- No inline comments
- No docstrings (except minimal class/function names if absolutely required for clarity)
- No block comments
- No TODO comments
- No copyright headers beyond minimal project identification
- No explanatory comments

### Rationale

Code must appear naturally written by a human developer without AI-style explanations.

### Exceptions (Minimal)

**Only if absolutely critical for correctness:**

- License header if required by submission
- Configuration file format explanations if non-obvious
- Regex pattern explanations only if pattern is complex and non-standard

**Even then, prefer:**

- Self-documenting code with clear variable/function names
- Extracting complex logic to well-named functions

### Examples

**WRONG:**

```python
# Calculate the average flowrate from the dataframe
avg_flowrate = df['Flowrate'].mean()

# Round to 2 decimal places for consistency
avg_flowrate = round(avg_flowrate, 2)
```

**CORRECT:**

```python
avg_flowrate = round(df['Flowrate'].mean(), 2)
```

**WRONG:**

```javascript
// Fetch dataset history from API
const response = await fetch('/api/history/', {
    headers: {
        'Authorization': `Token ${token}`  // Include auth token
    }
});
```

**CORRECT:**

```javascript
const response = await fetch('/api/history/', {
    headers: {
        'Authorization': `Token ${token}`
    }
});
```

## Code Structure Rules

### File Organization

**Keep Related Code Together:**

- API views in views.py
- Models in models.py
- Serializers in serializers.py
- React components in components/

**Avoid Excessive File Splitting:**

- Don't create separate files for tiny utilities
- Don't split components into multiple files unless they're large

### Function Length

**Guideline:**

- Keep functions under 50 lines when possible
- If longer, ensure it's necessarily complex
- Extract repeated patterns to helper functions

**Not a Hard Rule:**

- Some functions naturally need more lines
- Don't split artificially to meet arbitrary line count

### Naming Conventions

**Be Specific:**

- `upload_csv()` not `handle_file()`
- `compute_averages()` not `process()`
- `generate_pdf_report()` not `create_output()`

**Avoid Generic Names:**

- Not: `data`, `result`, `temp`, `handler`, `manager`, `processor`
- Use: `dataset`, `response`, `avg_flowrate`, `upload_view`, `history_manager`

### Error Handling

**Handle Expected Errors:**

- File not found
- Invalid CSV format
- Network errors
- Authentication failures

**Don't Overdo It:**

- No try-except around every line
- Catch specific exceptions, not bare except
- Let unexpected errors propagate for debugging

## Implementation Discipline

### Read Specifications First

Before implementing any component:

1. Read relevant specification markdown files
2. Understand exact requirements
3. Plan implementation approach
4. Implement precisely to spec
5. Verify against spec

### No Assumptions

**If specification is unclear:**

- Implement the simplest interpretation
- Prefer explicit over implicit behavior
- Document assumption in README if critical

**Never assume:**

- "The user probably wants X feature too"
- "This endpoint should probably also do Y"
- "We should add Z for better UX"

**Stick to specification strictly.**

### Verification Checklist

After implementing each component, verify:

- [ ] All specified features present
- [ ] No extra features added
- [ ] No comments in code
- [ ] Code follows style rules
- [ ] Error handling for specified cases
- [ ] API responses match specification
- [ ] Database schema matches specification

## Testing Requirements

### What to Test

**Backend:**

- CSV upload with valid file
- CSV upload with invalid file
- Authentication success and failure
- History retrieval
- PDF generation

**Frontend (Web):**

- Login flow
- File upload
- Chart rendering
- History display

**Frontend (Desktop):**

- Login dialog
- File upload
- Chart display
- PDF save

### Testing Approach

**Manual Testing Preferred:**

- Task does not require automated tests
- Focus on functionality, not test coverage

**If Writing Tests:**

- Keep tests simple and focused
- Test critical paths only
- No comments in test code either

## Git and Version Control

### Commit Messages

**Format:**

```
Add CSV upload endpoint

Implement file validation and Pandas parsing
```

**Rules:**

- First line: Brief summary (50 chars)
- Blank line
- Detailed explanation if needed (72 chars per line)
- No commit message templates or automated tags

### Repository Structure

```
project-root/
├── backend/
│   ├── manage.py
│   ├── config/
│   └── api/
├── web/
│   ├── src/
│   ├── public/
│   └── package.json
├── desktop/
│   ├── main.py
│   └── ui/
├── sample_equipment_data.csv
├── README.md
└── requirements.txt
```

### .gitignore

**Include:**

- Python: `__pycache__/`, `*.pyc`, `db.sqlite3`, `*.egg-info/`
- Node: `node_modules/`, `build/`, `.env`
- OS: `.DS_Store`, `Thumbs.db`
- IDE: `.vscode/`, `.idea/`, `*.swp`

## README Requirements

### Required Sections

1. **Project Title and Description**
2. **Tech Stack**
3. **Setup Instructions** (critical)
   - Backend setup
   - Web frontend setup
   - Desktop frontend setup
4. **Running the Application**
   - Start backend server
   - Start web frontend
   - Launch desktop application
5. **Testing with Sample Data**
6. **API Documentation** (brief)
7. **Submission Details** (optional)

### Setup Instructions Must Include

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Web Frontend:**

```bash
cd web
npm install
npm start
```

**Desktop Frontend:**

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

### README Style

- Clear, concise instructions
- Step-by-step format
- Assume user is technical but not familiar with project
- No marketing language or excessive formatting
- No emojis or informal tone

## Deployment Considerations

### Web Deployment (Optional)

**If deploying:**

- Build optimized production bundle
- Configure CORS for production domain
- Use environment variables for API URL
- Include deployment link in submission

**Not required but recommended for bonus points**

### Backend Deployment (Optional)

**Not expected for this task**

**If doing it anyway:**

- Use proper WSGI server (Gunicorn)
- Configure static file serving
- Use PostgreSQL instead of SQLite for production
- Set DEBUG=False

## Decision-Making Framework

### When Specification is Ambiguous

**Priority Order:**

1. Most conservative interpretation
2. Simplest implementation
3. Most common practice
4. Document decision in README

**Example:**

Spec says "basic authentication" without details

**Options:**

a) Token-based (REST Framework standard)
b) Session-based (Django default)
c) HTTP Basic Auth (literal interpretation)

**Choose:** Token-based (most common for REST APIs, explicit in many REST guides)

### When Multiple Approaches Exist

**Criteria:**

1. Simpler code
2. Fewer dependencies
3. More maintainable
4. Better error messages
5. Performance (only if significant difference)

**Example:**

PDF generation library choice

**Options:**

a) ReportLab (pure Python, widely used)
b) WeasyPrint (HTML to PDF, more dependencies)
c) fpdf (simple but limited)

**Choose:** ReportLab (balance of simplicity and capability)

## Quality Standards

### Code Must Be

- Readable by human developers
- Free of obvious bugs
- Properly structured
- Following language conventions
- Consistent in style throughout

### Code Must NOT Be

- Overly clever or terse
- Deeply nested or complex
- Filled with magic numbers
- Using obscure language features without reason
- Commented with AI-style explanations

## Final Checklist Before Submission

- [ ] All required features implemented
- [ ] No extra features added
- [ ] No comments anywhere in code
- [ ] Code follows style guidelines
- [ ] README has complete setup instructions
- [ ] Sample CSV file included
- [ ] All three components (backend, web, desktop) working
- [ ] Authentication working
- [ ] CSV upload working in both frontends
- [ ] Charts displaying correctly
- [ ] History showing last 5 datasets
- [ ] PDF generation working
- [ ] Repository clean (no unnecessary files)
- [ ] Demo video prepared (2-3 minutes)

## Prohibited Actions

**Never:**

- Add features not in specification
- Include comments in code
- Use AI-style variable naming
- Over-engineer simple solutions
- Ignore specification details
- Assume unstated requirements
- Add "nice-to-have" features
- Implement complex patterns unnecessarily

**Always:**

- Read specification files before coding
- Implement exactly what's specified
- Keep code clean and minimal
- Use natural human-written style
- Verify against specification
- Test critical functionality
- Follow established conventions
