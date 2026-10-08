from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Category, Product


class CategoryTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )

        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        response = self.client.post(
            '/api/categories/',
            {
                'name': 'Bebidas'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Bebidas')

    def test_list_categories(self):
        Category.objects.create(name='Bebidas')
        Category.objects.create(name='Comida')

        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class ProductTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='Comida'
        )

        self.product = Product.objects.create(
            name='Hamburguesa',
            category=self.category,
            description='Hamburguesa de carne',
            price=120.00,
            is_active=True
        )

    def test_create_product(self):
        response = self.client.post(
            '/api/products/',
            {
                'name': 'Pizza',
                'description': 'Pizza de pepperoni',
                'price': 150.00,
                'category': self.category.id
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Pizza')

    def test_list_products(self):
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Hamburguesa')

    def test_update_product(self):
        response = self.client.put(
            f'/api/products/{self.product.id}/',
            {
                'name': 'Hamburguesa Especial',
                'description': 'Hamburguesa especial de carne',
                'price': 180.00,
                'category': self.category.id
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['name'],
            'Hamburguesa Especial'
        )
        self.assertEqual(
            response.data['description'],
            'Hamburguesa especial de carne'
        )

    def test_delete_product(self):
        response = self.client.delete(
            f'/api/products/{self.product.id}/'
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Product.objects.filter(id=self.product.id).exists()
        )

    def test_precio_final_autenticado(self):
        response = self.client.get(
            f'/api/products/{self.product.id}/precio-final/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            f'/api/products/{self.product.id}/precio-final/'
        )

        self.assertEqual(response.status_code, 401)