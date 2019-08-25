from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status


class LoginTestCase(TestCase):
    def setUp(self):
        fake = Faker()
        email = fake.email()
        self.test_email = email
        self.password = 'testpassword'
        self.test_user = User.objects.create_user(email, email, self.password)
        # URL for login.
        self.login_url = reverse('account-signin')

    def test_signin_with_valid_data(self):
        data = {
            'email': self.test_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_with_invalid_email(self):
        data = {
            'email': 'testing',
            'passsword': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_empty_email(self):
        data = {
            'email': '',
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_no_email(self):
        data = {
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_empty_password(self):
        data = {
            'email': self.test_email,
            'password': ''
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_wrong_password(self):
        data = {
            'email': self.test_email,
            'password': 'test'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_no_password(self):
        data = {
            'email': self.test_email
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
