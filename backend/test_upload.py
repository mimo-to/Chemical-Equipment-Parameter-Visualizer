import os
import requests
import io

base_url = 'http://127.0.0.1:8000'
token = '4277e878474ff4aa917c9b937b71805a51fa3716'
headers = {'Authorization': f'Token {token}'}

csv_path = os.path.join('..', 'sample_equipment_data.csv')
with open(csv_path, 'rb') as f:
    files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
    r = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)

print(r.status_code)
if r.status_code == 201:
    print(r.json()['id'])

files = {'file': ('test.csv', io.BytesIO(b'Equipment Name,Type,Flowrate,Pressure,Temperature\nP1,Pump,100,10,50'), 'text/csv')}
r2 = requests.post(f'{base_url}/api/upload/', headers=headers, files=files)
print(r2.status_code)
print(r2.json().get('id'))
