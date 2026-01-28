import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import EquipmentDataset

EquipmentDataset.objects.all().delete()
User.objects.filter(username='history_test').delete()

user = User.objects.create_user(username='history_test', password='password')
token = Token.objects.create(user=user)
client = Client()
headers = {'HTTP_AUTHORIZATION': f'Token {token.key}'}

csv_content = b'Equipment Name,Type,Flowrate,Pressure,Temperature\nP1,Pump,100,10,50'

ids = []
for i in range(7):
    f = io.BytesIO(csv_content)
    f.name = f'file_{i}.csv'
    r = client.post('/api/upload/', {'file': f}, **headers)
    assert r.status_code == 201
    ids.append(r.json()['id'])

response = client.get('/api/history/')
assert response.status_code == 401

response = client.get('/api/history/', **headers)
assert response.status_code == 200

data = response.json()
assert len(data) == 5

received_ids = [item['id'] for item in data]
expected_ids = list(reversed(ids[-5:]))

assert received_ids == expected_ids
assert 'total_count' in data[0]

print("History endpoint verified.")
