from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from ...models import Contact
from ...models import EmailAddress
from ...models import PhoneNumber


class ContactTestCase(TestCase):
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
        self.create_contact = reverse('contact-create')
        self.retrieve_contact = "/contact/{}".format(self.contact.id)
        self.update_contact = "/contact/{}/update".format(self.contact.id)
        self.partial_update_contact = "/contact/{}/basic-update".format(self.contact.id)
        self.delete_contact = "/contact/{}/delete".format(self.contact.id)

    def test_create_contact_with_valid_data(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contact_without_authorization(self):
        fake = Faker()

        data = {
            'first_name': "",
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        headers = {}
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contact_with_empty_first_name(self):
        fake = Faker()

        data = {
            'first_name': "",
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_no_first_name(self):
        fake = Faker()

        data = {
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_empty_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': "",
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_no_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_no_email(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': "",
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_invalid_email(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.first_name(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_empty_company(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': "",
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contact_with_empty_designation(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': "",
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contact_with_invalid_email_type(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'jkjkjkjjkjk'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_invalid_phone_number_type(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'homegghghghghgh',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_first_name(self):
        fake = Faker()

        data = {
            'first_name': "testtest" * 50,
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': "testtest" * 50,
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_middle_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': "testtest" * 50,
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_nickname(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': "testtest" * 50,
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_company(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': "testtest" * 50,
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_long_designation(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': "testtest" * 50,
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.create_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.post(self.create_contact, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_contact_with_valid_data(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.get(self.retrieve_contact, {}, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_contact_without_authorization(self):
        headers = {}
        response = self.client.get(self.retrieve_contact, {}, **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_contact_with_invalid_id(self):
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.get(self.retrieve_contact + "988", {}, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_contact_with_valid_data(self):
        user_data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact_with_different_user(self):
        fake = Faker()
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        response = self.client.post(self.create_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_contact_without_authorization(self):
        headers = {}

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_contact_with_no_first_name(self):
        fake = Faker()

        data = {
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_empty_first_name(self):
        fake = Faker()

        data = {
            'first_name': "",
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_no_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_empty_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': "",
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_no_email(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': "",
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_invalid_email(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.first_name(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_empty_company(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': "",
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact_with_empty_designation(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': "",
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact_with_invalid_email_type(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'jkjkjkjjkjk'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_invalid_phone_number_type(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'homegghghghghgh',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_first_name(self):
        fake = Faker()

        data = {
            'first_name': "testtest" * 50,
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_last_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': "testtest" * 50,
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_middle_name(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': "testteest" * 50,
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_nickname(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': "testtest" * 50,
            'company': fake.company(),
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_company(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': "testtest" * 50,
            'designation': fake.job(),
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_long_designation(self):
        fake = Faker()

        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': "testtest" * 50,
            'phone_number': fake.phone_number(),
            'phone_number_type': 'home',
            'email_address': fake.email(),
            'email_type': 'home'
        }
        email = self.user_email
        user_data = {
            'email': email,
            'password': self.password
        }

        user_response = self.client.post(self.login_url, user_data, format='json')
        token = user_response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }
        response = self.client.put(self.update_contact, data, format='json', content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_contact_with_valid_data(self):
        user_data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job()
        }
        response = self.client.patch(self.partial_update_contact, data, format='json', content_type='application/json',
                                     **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_contact_without_authorizarion(self):
        headers = {}

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job()
        }
        response = self.client.patch(self.partial_update_contact, data, format='json', content_type='application/json',
                                     **headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_contact_with_different_user(self):
        fake = Faker()
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        response = self.client.post(self.create_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        fake = Faker()
        data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.last_name(),
            'nickname': fake.first_name(),
            'company': fake.company(),
            'designation': fake.job()
        }
        response = self.client.put(self.partial_update_contact, data, format='json', content_type='application/json',
                                   **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_contact_with_valid_data(self):
        user_data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(self.login_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        response = self.client.delete(self.delete_contact, {}, format='json', content_type='application/json',
                                      **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_contact_without_authorizarion(self):
        headers = {}
        response = self.client.delete(self.delete_contact, {}, format='json', content_type='application/json',
                                      **headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_contact_with_different_user(self):
        fake = Faker()
        email = fake.email()
        user_data = {
            'username': email,
            'email': email,
            'password': self.password
        }

        response = self.client.post(self.create_url, user_data, format='json')
        token = response.json().get('token')
        headers = {
            'HTTP_AUTHORIZATION': "Token " + token
        }

        response = self.client.delete(self.delete_contact, {}, format='json', content_type='application/json',
                                      **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
