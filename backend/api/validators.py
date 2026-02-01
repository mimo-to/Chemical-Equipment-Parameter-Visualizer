import pandas as pd
from django.core.exceptions import ValidationError
from .constants import (
    MAX_UPLOAD_SIZE,
    REQUIRED_COLUMNS,
    NUMERIC_COLUMNS,
    ERROR_MESSAGES
)

def validate_file_size(file):
    if file.size > MAX_UPLOAD_SIZE:
        max_mb = MAX_UPLOAD_SIZE / (1024 * 1024)
        raise ValidationError(ERROR_MESSAGES['file_too_large'].format(max_mb=max_mb))

def validate_file_extension(file):
    if not file.name.endswith('.csv'):
        raise ValidationError(ERROR_MESSAGES['invalid_extension'])

def validate_csv_structure(df):
    if df.empty:
        raise ValidationError(ERROR_MESSAGES['empty_file'])

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValidationError(ERROR_MESSAGES['missing_columns'].format(
            cols=', '.join(missing_cols),
            required=', '.join(REQUIRED_COLUMNS)
        ))
    
    extra_cols = [col for col in df.columns if col not in REQUIRED_COLUMNS]
    if extra_cols:
        raise ValidationError(ERROR_MESSAGES['extra_columns'].format(
            cols=', '.join(extra_cols),
            allowed=', '.join(REQUIRED_COLUMNS)
        ))

def validate_csv_content(df):
    for col in NUMERIC_COLUMNS:
        if df[col].dtype == 'object':
             temp_col = pd.to_numeric(df[col], errors='coerce')
             nan_mask = temp_col.isna()
             if nan_mask.any():
                 invalid_rows = [r + 2 for r in df.index[nan_mask].tolist()[:5]]
                 raise ValidationError(ERROR_MESSAGES['invalid_numeric'].format(
                     col=col,
                     rows=invalid_rows
                 ))
        
        if df[col].isna().any():
             invalid_rows = [r + 2 for r in df.index[df[col].isna()].tolist()[:5]]
             raise ValidationError(ERROR_MESSAGES['empty_values'].format(
                 col=col,
                 rows=invalid_rows
             ))
             
        if not pd.api.types.is_numeric_dtype(df[col]):
             raise ValidationError(ERROR_MESSAGES['not_numeric_type'].format(col=col))
