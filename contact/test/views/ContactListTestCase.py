from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from ...models import Contact
from ...models import EmailAddress
from ...models import PhoneNumber


class ContactListTestCase(TestCase):
    def setUp(self):
        fake = Faker()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.middle_name = fake.last_name()
        self.nickname = fake.name()
        self.company = fake.company()
        self.designation = fake.job()
        self.phone_number = fake.phone_number()
        self.email_address = fake.email()

        self.user_email = fake.email()
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.user_email, self.user_email, self.password)

        contact_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'nickname': self.nickname,
            'company': self.company,
            'designation': self.designation,
            'user': self.user
        }
        self.contact = Contact.objects.create(**contact_data)
        self.phone_contact = PhoneNumber.objects.create(**{
            'phone_number': self.phone_number,
            'type': 'other',
            'contact_object': self.contact
        })
        self.email_contact = EmailAddress.objects.create(**{
            'email_address': self.email_address,
            'type': 'other',
            'contact_object': self.contact
        })
        # URL for creating an account.
        self.create_url = reverse('account-register')
        self.login_url = reverse('account-signin')
        # Contact URLs.
        self.create_list = reverse('contact-list')

    def test_list_contact_with_valid_data(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        data = {
            'page': 1
        }
        response = self.client.get(self.create_list, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contact_with_invalid_page(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        data = {
            'page': 100
        }
        response = self.client.get(self.create_list, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_contact_without_page(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        response = self.client.get(self.create_list, data={}, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contact_with_existing_email(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        data = {
            'email': self.email_address
        }
        response = self.client.get(self.create_list, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contact_with_non_existing_email(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        data = {
            'email': "jhhjfdjfgjkfgkj@jhfgjhfgjhgfhj.co"
        }
        response = self.client.get(self.create_list, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_contact_with_empty_email(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        data = {
            'email': ""
        }
        response = self.client.get(self.create_list, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
