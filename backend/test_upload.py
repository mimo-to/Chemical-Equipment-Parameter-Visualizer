import requests
import os
import io

base_url = 'http://127.0.0.1:8000'
token = '4277e878474ff4aa917c9b937b71805a51fa3716'
headers = {'Authorization': f'Token {token}'}

print('=== Phase 4 CSV Parsing and Validation Tests ===\n')

print('Test 1: Upload empty CSV')
empty_csv = io.BytesIO(b'')
files = {'file': ('empty.csv', empty_csv, 'text/csv')}
r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400')
print(f'Pass: {r.status_code == 400}\n')

print('Test 2: Upload CSV with missing columns')
missing_cols_csv = io.BytesIO(b'Equipment Name,Type\nPump A,Centrifugal')
files = {'file': ('missing_cols.csv', missing_cols_csv, 'text/csv')}
r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400 with missing column names')
print(f'Pass: {r.status_code == 400 and "Missing required columns" in r.json().get("error", "")}\n')

print('Test 3: Upload CSV with invalid numeric values')
invalid_numeric_csv = io.BytesIO(b'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump A,Centrifugal,100,invalid,75')
files = {'file': ('invalid_numeric.csv', invalid_numeric_csv, 'text/csv')}
r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400 with row and column info')
print(f'Pass: {r.status_code == 400 and "Invalid numeric value" in r.json().get("error", "")}\n')

print('Test 4: Upload valid CSV (sample_equipment_data.csv)')
csv_path = os.path.join('..', 'sample_equipment_data.csv')
with open(csv_path, 'rb') as f:
    files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
    r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 201')
print(f'Pass: {r.status_code == 201}\n')

print('Test 5: Upload CSV with only headers (empty data)')
headers_only_csv = io.BytesIO(b'Equipment Name,Type,Flowrate,Pressure,Temperature\n')
files = {'file': ('headers_only.csv', headers_only_csv, 'text/csv')}
r = requests.post(f'{base_url}/api/upload/', headers={'Authorization': f'Token {token}'}, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400 (empty)')
print(f'Pass: {r.status_code == 400}\n')

print('=== All Tests Summary ===')
print('All tests should show Pass: True')
