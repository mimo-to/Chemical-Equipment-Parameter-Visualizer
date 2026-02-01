MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

REQUIRED_COLUMNS = [
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature'
]

NUMERIC_COLUMNS = [
    'Flowrate',
    'Pressure',
    'Temperature'
]

ERROR_MESSAGES = {
    'file_too_large': (
        'File exceeds {max_mb}MB limit. '
        'Split your data into smaller files or remove unnecessary rows.'
    ),
    'invalid_extension': (
        'Invalid file type. Only .csv files are supported. '
        'Save your spreadsheet as CSV (comma-separated values).'
    ),
    'empty_file': (
        'CSV file is empty. Add data rows below the header line. '
        'See sample_equipment_data.csv for the expected format.'
    ),
    'missing_columns': (
        'Missing required columns: {cols}. '
        'Required columns are: {required}. Check column names match exactly.'
    ),
    'extra_columns': (
        'Unexpected columns found: {cols}. '
        'Only these columns are allowed: {allowed}. Remove extra columns.'
    ),
    'invalid_numeric': (
        'Invalid numeric value in column "{col}" at row(s): {rows}. '
        'Ensure values are numbers (e.g., 10.5). Remove text or special characters.'
    ),
    'empty_values': (
        'Empty or missing values in column "{col}" at row(s): {rows}. '
        'Fill in all required fields before uploading.'
    ),
    'not_numeric_type': (
        'Column "{col}" must contain numeric data. '
        'Check that values are numbers, not text.'
    ),
}
