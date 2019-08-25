from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status


class RegisterTestCase(TestCase):
    def setUp(self):
        fake = Faker()
        email = fake.email()
        self.test_email = email
        self.password = 'testpassword'
        self.test_user = User.objects.create_user(email, email, self.password)
        # URL for creating an account.
        self.create_url = reverse('account-register')

    def test_create_user_with_valid_data(self):
        fake = Faker()
        email = fake.email()
        data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.json()['email'], email)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': self.test_email,
            'email': self.test_email,
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': self.test_email,
            'email': 'testing',
            'passsword': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_email(self):
        data = {
            'username': self.test_email,
            'email': '',
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_email(self):
        data = {
            'username': self.test_email,
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_username(self):
        data = {
            'username': '',
            'email': self.test_email,
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_username(self):
        data = {
            'email': self.test_email,
            'password': self.password
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_password(self):
        data = {
            'username': self.test_email,
            'email': self.test_email,
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_min_len_password(self):
        data = {
            'username': self.test_email,
            'email': self.test_email,
            'password': 'test'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_password(self):
        data = {
            'username': self.test_email,
            'email': self.test_email
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
