from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AuthTests(APITestCase):
    def setUp(self):
        # Use direct URL paths for simplicity
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'strongpass123'
        }
        # Register a user for login tests
        self.client.post(self.register_url, self.user_data, format='json')
        login_resp = self.client.post(self.login_url, {'email': self.user_data['email'], 'password': self.user_data['password']}, format='json')
        self.access_token = login_resp.data['tokens']['access']
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

    def test_successful_registration(self):
        resp = self.client.post(self.register_url, {
            'name': 'Alice',
            'email': 'alice@example.com',
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', resp.data)
        self.assertNotIn('password', resp.data.get('user', {}))

    def test_registration_missing_fields(self):
        resp = self.client.post(self.register_url, {'email': 'bob@example.com'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_email(self):
        resp = self.client.post(self.register_url, {
            'name': 'Invalid Email',
            'email': 'not-an-email',
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_registration(self):
        # First registration already done in setUp
        resp = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resp.data)

    def test_password_minimum_length(self):
        resp = self.client.post(self.register_url, {
            'name': 'Short Pass',
            'email': 'short@example.com',
            'password': 'short'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', resp.data)

    def test_successful_login(self):
        resp = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', resp.data)
        self.assertIn('access', resp.data['tokens'])

    def test_login_incorrect_password(self):
        resp = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': 'wrongpass'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unregistered_email(self):
        resp = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'doesntmatter'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_protected_endpoint_without_token(self):
        resp = self.client.get('/api/patients/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
