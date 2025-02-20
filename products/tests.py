from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import Product,Category,Review

class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Category1')
        self.product1 = Product.objects.create(name='Product1',category=self.category1, price=5000)
        self.product2 = Product.objects.create(name='Product2',category=self.category1, price=6000)
        self.review1 = Review.objects.create(name='Product1',rating=5)
        self.review2 = Review.objects.create(name='Product1',rating=4)
        self.client = APIClient()

    def test_list_product(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_product_with_category_filter(self):
        response = self.client.get(reverse('product_list'), {'category': self.category1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_product(self):
        response = self.client.get(reverse('product_top_rated'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('product',response.data)
        self.assertIn('related_product',response.data)

    def test_top_rated(self):
        response = self.client.get(reverse('product-top_rated'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_average_rating(self):
        response = self.client.get('product-average_rating', args=[self.product1.id])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        avg_rating =(self.review1.rating * self.review2.rating) / 2
        self.assertEqual(response.data['average_rating'], avg_rating)