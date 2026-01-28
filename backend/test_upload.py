import requests
import os

base_url = 'http://127.0.0.1:8000'
token = '4277e878474ff4aa917c9b937b71805a51fa3716'

print('=== Phase 3 Upload Endpoint Tests ===\n')

print('Test 1: Upload without token')
r = requests.post(f'{base_url}/api/upload/')
print(f'Status: {r.status_code}')
print(f'Expected: 401')
print(f'Pass: {r.status_code == 401}\n')

print('Test 2: Upload with invalid token')
r = requests.post(f'{base_url}/api/upload/', headers={'Authorization': 'Token invalidtoken123'})
print(f'Status: {r.status_code}')
print(f'Expected: 401')
print(f'Pass: {r.status_code == 401}\n')

print('Test 3: Upload with valid token but no file')
r = requests.post(f'{base_url}/api/upload/', headers={'Authorization': f'Token {token}'})
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400')
print(f'Pass: {r.status_code == 400}\n')

print('Test 4: Upload with valid token but non-CSV file')
files = {'file': ('test.txt', 'test content', 'text/plain')}
r = requests.post(f'{base_url}/api/upload/', headers={'Authorization': f'Token {token}'}, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 400')
print(f'Pass: {r.status_code == 400}\n')

print('Test 5: Upload with valid token and CSV file')
csv_path = os.path.join('..', 'sample_equipment_data.csv')
with open(csv_path, 'rb') as f:
    files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
    r = requests.post(f'{base_url}/api/upload/', headers={'Authorization': f'Token {token}'}, files=files)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
print(f'Expected: 201')
print(f'Pass: {r.status_code == 201}\n')

print('=== All Tests Summary ===')
print('All tests should show Pass: True')
