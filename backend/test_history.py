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
for i in range(5):
    f = io.BytesIO(csv_content)
    f.name = f'file_{i}.csv'
    r = client.post('/api/upload/', {'file': f}, **headers)
    assert r.status_code == 201
    ids.append(r.json()['id'])

assert EquipmentDataset.objects.count() == 5

f = io.BytesIO(csv_content)
f.name = 'file_5.csv'
r = client.post('/api/upload/', {'file': f}, **headers)
assert r.status_code == 201
new_id = r.json()['id']

assert EquipmentDataset.objects.count() == 5
current_ids = list(EquipmentDataset.objects.values_list('id', flat=True))

assert ids[0] not in current_ids
assert new_id in current_ids
assert set(current_ids) == set(ids[1:] + [new_id])

print("History limit verified.")
