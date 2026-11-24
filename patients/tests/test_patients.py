from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class PatientAPITests(APITestCase):
    def setUp(self):
        # Register and obtain token for user A
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.user_a = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'password': 'strongpass123'
        }
        self.client.post(self.register_url, self.user_a, format='json')
        resp = self.client.post(self.login_url, {'email': self.user_a['email'], 'password': self.user_a['password']}, format='json')
        self.token_a = resp.data['tokens']['access']
        self.auth_a = {'HTTP_AUTHORIZATION': f'Bearer {self.token_a}'}
        # Register and obtain token for user B
        self.user_b = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'password': 'strongpass123'
        }
        self.client.post(self.register_url, self.user_b, format='json')
        resp = self.client.post(self.login_url, {'email': self.user_b['email'], 'password': self.user_b['password']}, format='json')
        self.token_b = resp.data['tokens']['access']
        self.auth_b = {'HTTP_AUTHORIZATION': f'Bearer {self.token_b}'}
        # Create a patient for user A
        self.patient_a_data = {
            'name': 'Patient A',
            'age': 30,
            'gender': 'Male',
            'phone_number': '1234567890'
        }
        self.client.post('/api/patients/', self.patient_a_data, format='json', **self.auth_a)
        # Create a patient for user B
        self.patient_b_data = {
            'name': 'Patient B',
            'age': 25,
            'gender': 'Female',
            'phone_number': '0987654321'
        }
        self.client.post('/api/patients/', self.patient_b_data, format='json', **self.auth_b)
        # Retrieve IDs
        self.patient_a_id = self.client.get('/api/patients/', **self.auth_a).data[0]['id']
        self.patient_b_id = self.client.get('/api/patients/', **self.auth_b).data[0]['id']

    def test_create_patient_authenticated(self):
        resp = self.client.post('/api/patients/', {
            'name': 'New Patient',
            'age': 40,
            'gender': 'Other',
            'phone_number': '1112223333'
        }, format='json', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], 'New Patient')

    def test_patient_list_ownership(self):
        resp = self.client.get('/api/patients/', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)  # user A should see only their own patient
        for p in resp.data:
            self.assertTrue(p['name'] == 'Patient A' or p['name'] == 'Patient B')
        # Ensure B cannot see A's patients
        resp_b = self.client.get('/api/patients/', **self.auth_b)
        self.assertEqual(resp_b.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_b.data), 1)
        self.assertEqual(resp_b.data[0]['name'], 'Patient B')

    def test_retrieve_patient_detail(self):
        resp = self.client.get(f'/api/patients/{self.patient_a_id}/', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Patient A')

    def test_update_patient_put(self):
        resp = self.client.put(f'/api/patients/{self.patient_a_id}/', {
            'name': 'Patient A Updated',
            'age': 31,
            'gender': 'Male',
            'phone_number': '1234567890'
        }, format='json', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Patient A Updated')

    def test_update_patient_patch(self):
        resp = self.client.patch(f'/api/patients/{self.patient_a_id}/', {'age': 32}, format='json', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['age'], 32)

    def test_delete_patient(self):
        resp = self.client.delete(f'/api/patients/{self.patient_a_id}/', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Verify it no longer exists
        resp = self.client.get(f'/api/patients/{self.patient_a_id}/', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        resp = self.client.get('/api/patients/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cross_user_access_denied(self):
        # User B attempts to retrieve A's patient
        resp = self.client.get(f'/api/patients/{self.patient_a_id}/', **self.auth_b)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        # Update attempt
        resp = self.client.patch(f'/api/patients/{self.patient_a_id}/', {'age': 99}, format='json', **self.auth_b)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        # Delete attempt
        resp = self.client.delete(f'/api/patients/{self.patient_a_id}/', **self.auth_b)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_patient_data(self):
        # Missing required field 'name'
        resp = self.client.post('/api/patients/', {'age': 20, 'gender': 'Male', 'phone_number': '111'}, format='json', **self.auth_a)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
