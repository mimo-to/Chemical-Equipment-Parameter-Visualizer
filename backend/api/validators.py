import pandas as pd
from django.core.exceptions import ValidationError
from .constants import MAX_UPLOAD_SIZE, REQUIRED_COLUMNS, NUMERIC_COLUMNS

def validate_file_size(file):
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(f"File too large. Max size is {MAX_UPLOAD_SIZE / (1024 * 1024)}MB.")

def validate_file_extension(file):
    if not file.name.endswith('.csv'):
        raise ValidationError("Invalid file type. Only .csv files are allowed.")

def validate_csv_structure(df):
    if df.empty:
        raise ValidationError("CSV file is empty.")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValidationError(f"Missing columns: {', '.join(missing_cols)}")
    
    extra_cols = [col for col in df.columns if col not in REQUIRED_COLUMNS]
    if extra_cols:
        raise ValidationError(f"Unexpected columns: {', '.join(extra_cols)}")

def validate_csv_content(df):
    for col in NUMERIC_COLUMNS:
        if df[col].dtype == 'object':
             temp_col = pd.to_numeric(df[col], errors='coerce')
             nan_mask = temp_col.isna()
             if nan_mask.any():
                 invalid_rows = [r + 2 for r in df.index[nan_mask].tolist()[:5]]
                 raise ValidationError(f'Invalid numeric value in column "{col}" at row(s): {invalid_rows}')
        
        if df[col].isna().any():
             invalid_rows = [r + 2 for r in df.index[df[col].isna()].tolist()[:5]]
             raise ValidationError(f'Empty or invalid value in column "{col}" at row(s): {invalid_rows}')
             
        if not pd.api.types.is_numeric_dtype(df[col]):
             raise ValidationError(f'Column "{col}" must contain numeric data.')
