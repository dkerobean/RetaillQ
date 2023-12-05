from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import Products, CustomUser


class ProductTestCase(APITestCase):
    def setUp(self):

        # create a user for testing
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            organization_name="testorganization",
            country="testcountry",
        )

        # authenticate the user
        self.client.force_authenticate(user=self.user)

        # create a product for testing
        self.product_data = {
            'user': self.user,
            'name': 'Test Product',
            'price': '12.99',
            'quantity': 1,
        }
        self.product = Products.objects.create(**self.product_data)

        self.url = reverse('product-detail', kwargs={'pk': self.product.id}) # noqa

    def test_create_product(self):
        new_product_data = {
            'user': self.user.id,
            'name': 'new product',
            'price': '12.99',
            'quantity': 1,
        }

        response = self.client.post(reverse('products'), new_product_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(), 2)

    def test_retrieve_product(self):

        response = self.client.get(reverse('products'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Product')


    def test_update_product(self):
        updated_product_data = {
            'user': self.user.id,
            'name': 'Updated Product',
            'quantity': 15,
            'price': 25.99,
        }

        response = self.client.put(self.url, updated_product_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Products.objects.count(), 0)
