from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken  # noqa


class UserRegistrationLoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('user-register')
        self.login_url = reverse('token-obtain-pair')

        # sample registration data
        self.user_data = {
            "organization_name": "Test Organization",
            "email": "test1@example.com",
            "password": "testpassword",
            "country": "testcountry"
        }

        # sample user for testing purposes
        self.user = CustomUser.objects.create_user(
            organization_name=self.user_data.get('organization_name'),
            email=self.user_data.get('email'),
            password=self.user_data.get('password'),
            country=self.user_data.get('country')
        )

    def test_user_registration(self):
        # response = self.client.post(self.registration_url, self.user_data, format='json') # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # noqa
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json') # noqa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('access', response.data)
