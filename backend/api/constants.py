MAX_UPLOAD_SIZE = 10 * 1024 * 1024
HISTORY_LIMIT = 5

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
    'file_too_large': 'File exceeds {max_mb}MB limit.',
    'invalid_extension': 'Only .csv files allowed.',
    'empty_file': 'CSV file is empty.',
    'missing_columns': 'Missing columns: {cols}',
    'extra_columns': 'Unexpected columns: {cols}',
    'invalid_numeric': 'Invalid numeric value in column "{col}" at row(s): {rows}',
    'empty_values': 'Missing values in column "{col}" at row(s): {rows}',
    'not_numeric_type': 'Column "{col}" must be numeric.',
}
