import requests
import os

base_url = 'http://127.0.0.1:8000'
token = '4277e878474ff4aa917c9b937b71805a51fa3716'
headers = {'Authorization': f'Token {token}'}

print('=== Phase 6 Database Storage and Response Tests ===\n')

print('Test 1: Upload valid CSV and check response')
csv_path = os.path.join('..', 'sample_equipment_data.csv')
with open(csv_path, 'rb') as f:
    files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
    r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)

print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print()

if r.status_code == 201:
    data = r.json()
    print('=== Response Field Validation ===')
    print(f'Has id: {"id" in data}')
    print(f'Has filename: {"filename" in data}')
    print(f'Has uploaded_at: {"uploaded_at" in data}')
    print(f'Has total_count: {"total_count" in data}')
    print(f'Has avg_flowrate: {"avg_flowrate" in data}')
    print(f'Has avg_pressure: {"avg_pressure" in data}')
    print(f'Has avg_temperature: {"avg_temperature" in data}')
    print(f'Has type_distribution: {"type_distribution" in data}')
    print()
    
    print('=== Field Values ===')
    print(f'id: {data.get("id")}')
    print(f'filename: {data.get("filename")}')
    print(f'uploaded_at: {data.get("uploaded_at")}')
    print(f'total_count: {data.get("total_count")}')
    print(f'avg_flowrate: {data.get("avg_flowrate")}')
    print(f'avg_pressure: {data.get("avg_pressure")}')
    print(f'avg_temperature: {data.get("avg_temperature")}')
    print(f'type_distribution: {data.get("type_distribution")}')
    print()
    
    print('=== ISO 8601 Format Check ===')
    uploaded_at = data.get('uploaded_at', '')
    print(f'uploaded_at contains "T": {"T" in uploaded_at}')
    print(f'uploaded_at format looks correct: {len(uploaded_at) > 10}')
    print()

print('Test 2: Upload another CSV to verify multiple records')
import io
test_csv = io.BytesIO(b'Equipment Name,Type,Flowrate,Pressure,Temperature\nTest Pump,Pump,100,5,80')
files = {'file': ('test.csv', test_csv, 'text/csv')}
r2 = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(f'Status: {r2.status_code}')
print(f'Response: {r2.json()}')
print()

if r2.status_code == 201:
    data2 = r2.json()
    print(f'Second upload id: {data2.get("id")}')
    print(f'IDs are different: {data.get("id") != data2.get("id")}')
