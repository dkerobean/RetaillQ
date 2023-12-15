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
        self.client.force_authenticate(user=self.user)

        # create a product
        self.product_data = {
            'user': self.user,
            'name': 'Test Product',
            'price': '12.99',
            'quantity': 100,
        }

        self.product = Products.objects.create(**self.product_data)

        # create a new sale
        self.sale_data = {
            'user': self.user,
            'product': self.product,
            'quantity_sold': 1,
            'sale_date': '2013-12-01'
        }

        self.sale = Sale.objects.create(**self.sale_data)

        self.url = reverse('sale-detail', kwargs={'pk': self.sale.id})
        self.url2 = reverse('sale-single', kwargs={'pk': self.sale.id})

    def test_create_sale(self):
        new_sale = {
            'user': self.user.id,
            'product': self.product.id,
            'quantity_sold': 5,
            'sale_date': '2013-12-01'
        }

        response = self.client.post(reverse('sale'), data=new_sale, format='json')  # noqa

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 2)

    def test_retrieve_all_sales(self):

        response = self.client.get(reverse('sale'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['quantity_sold'], 1)

    def test_retrieve_one_sale(self):

        response = self.client.get(self.url2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity_sold'], 1)

    def test_update_sale(self):

        updated_sale = {
            'user': self.user.id,
            'product': self.product.id,
            'quantity_sold': 52,
            'sale_date': '2019-12-01'
        }

        response = self.client.put(self.url, updated_sale)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(response.data['quantity_sold'], 52)
