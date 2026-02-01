from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')

    def test_login_success(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        response = self.client.post('/api/login/', {})
        self.assertEqual(response.status_code, 400)


class UploadViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.valid_csv = b'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-1,Pump,100.0,5.0,25.0\n'

    def test_upload_requires_auth(self):
        response = self.client.post('/api/upload/')
        self.assertEqual(response.status_code, 401)

    def test_upload_no_file(self):
        response = self.client.post(
            '/api/upload/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 400)

    def test_upload_valid_csv(self):
        csv_file = SimpleUploadedFile('test.csv', self.valid_csv, content_type='text/csv')
        response = self.client.post(
            '/api/upload/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 201)

    def test_upload_invalid_extension(self):
        txt_file = SimpleUploadedFile('test.txt', b'some text', content_type='text/plain')
        response = self.client.post(
            '/api/upload/',
            {'file': txt_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 400)


class HistoryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)

    def test_history_requires_auth(self):
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, 401)

    def test_history_returns_empty(self):
        response = self.client.get(
            '/api/history/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_history_returns_uploaded_datasets(self):
        csv_file = SimpleUploadedFile(
            'test.csv',
            b'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-1,Pump,100.0,5.0,25.0\n',
            content_type='text/csv'
        )
        self.client.post(
            '/api/upload/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        response = self.client.get(
            '/api/history/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)

    def test_report_requires_auth(self):
        response = self.client.get('/api/report/1/')
        self.assertEqual(response.status_code, 401)

    def test_report_not_found(self):
        response = self.client.get(
            '/api/report/999/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 404)


class CompareViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.csv_content = b'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-1,Pump,100.0,5.0,25.0\n'

    def test_compare_requires_auth(self):
        response = self.client.post('/api/compare/')
        self.assertEqual(response.status_code, 401)

    def test_compare_missing_ids(self):
        response = self.client.post(
            '/api/compare/',
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 400)

    def test_compare_not_found(self):
        response = self.client.post(
            '/api/compare/',
            {'dataset1': 999, 'dataset2': 998},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 404)

    def test_compare_success(self):
        csv1 = SimpleUploadedFile('test1.csv', self.csv_content, content_type='text/csv')
        csv2 = SimpleUploadedFile('test2.csv', self.csv_content, content_type='text/csv')
        
        r1 = self.client.post('/api/upload/', {'file': csv1}, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        r2 = self.client.post('/api/upload/', {'file': csv2}, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.post(
            '/api/compare/',
            {'dataset1': r1.json()['id'], 'dataset2': r2.json()['id']},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('comparison', response.json())

