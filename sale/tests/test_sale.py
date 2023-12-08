from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, Sale, Products


class SaleTestCase(APITestCase):
    def setUp(self):
        # create a new user
        self.user = CustomUser.objects.create(
            email="testuser@example.com",
            password="testpassword",
            organization_name="testorganization",
            country="testcountry",
        )

        # authenticate the user
        self.client.force_authentication(user=self.user)

        # create a product
        self.product_data = {
            'user': self.user,
            'name': 'Test Product',
            'price': '12.99',
            'quantity': 1,
        }

        self.product = Products.objects.create(**self.product_data)

        # create a new sale
        self.sale_data = {
            'user': self.user,
            'product': self.product,
            
        }