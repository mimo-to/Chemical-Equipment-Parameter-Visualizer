import pandas as pd
import io
from django.core.exceptions import ValidationError
from api.validators import validate_csv_structure, validate_csv_content

def test_structure():
    print("Testing Structure Validation...")
    
    # Valid
    df_valid = pd.DataFrame(columns=['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
    try:
        validate_csv_structure(df_valid)
        print("  [PASS] Valid structure accepted.")
    except Exception as e:
        print(f"  [FAIL] Valid structure rejected: {e}")

    # Missing Column
    df_missing = pd.DataFrame(columns=['Equipment Name', 'Type', 'Flowrate'])
    try:
        validate_csv_structure(df_missing)
        print("  [FAIL] Missing columns passed.")
    except ValidationError as e:
        print(f"  [PASS] Missing columns rejected: {e.message}")

    # Extra Column
    df_extra = pd.DataFrame(columns=['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature', 'Extra'])
    try:
        validate_csv_structure(df_extra)
        print("  [FAIL] Extra columns passed.")
    except ValidationError as e:
        print(f"  [PASS] Extra columns rejected: {e.message}")

def test_content():
    print("\nTesting Content Validation...")
    
    # Valid Content
    df_valid = pd.DataFrame({
        'Flowrate': [10.5, 20.0], 
        'Pressure': [100, 200], 
        'Temperature': [50.5, 60.0]
    })
    try:
        validate_csv_content(df_valid)
        print("  [PASS] Valid content accepted.")
    except Exception as e:
        print(f"  [FAIL] Valid content rejected: {e}")

    # Non-numeric
    df_bad_type = pd.DataFrame({
        'Flowrate': ['abc', 20.0], 
        'Pressure': [100, 200], 
        'Temperature': [50.5, 60.0]
    })
    try:
        validate_csv_content(df_bad_type)
        print("  [FAIL] Non-numeric passed.")
    except ValidationError as e:
        print(f"  [PASS] Non-numeric rejected: {e.message}")

    # Empty/NaN
    df_nan = pd.DataFrame({
        'Flowrate': [10.5, None], 
        'Pressure': [100, 200], 
        'Temperature': [50.5, 60.0]
    })
    try:
        validate_csv_content(df_nan)
        print("  [FAIL] NaN passed.")
    except ValidationError as e:
        print(f"  [PASS] NaN rejected: {e.message}")

if __name__ == "__main__":
    try:
        test_structure()
        test_content()
        print("\nAll tests completed.")
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
