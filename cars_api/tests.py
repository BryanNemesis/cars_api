from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .models import Car, Rating


class CarsApiTests(APITestCase):
    def setUp(self):
        client = APIClient(SERVER_NAME='localhost')
        c1 = Car.objects.create(make='Porsche', model='911')
        c2 = Car.objects.create(make='Aston Martin', model='Vanquish')
        Car.objects.create(make='Maserati', model='Quattroporte')
        Rating.objects.create(car=c1, rating=5)
        Rating.objects.create(car=c2, rating=4)
        Rating.objects.create(car=c2, rating=5)


    def test_car_list(self):
        url = reverse('car-list-and-create')
        response = self.client.get(url)
        expected_data = [
            {'id': 1, 'make': 'Porsche', 'model': '911', 'avg_rating': 5},
            {'id': 2, 'make': 'Aston Martin', 'model': 'Vanquish', 'avg_rating': 4.5},
            {'id': 3, 'make': 'Maserati', 'model': 'Quattroporte', 'avg_rating': None},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        

    def test_car_create(self):
        url = reverse('car-list-and-create')
        expected_data = {'id': 4, 'make': 'Ferrari', 'model': 'Testarossa', 'avg_rating': None}
        data = {'make': 'Ferrari', 'model': 'Testarossa'}
        response = self.client.post(url, data)
        created_car = Car.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(created_car.make, 'Ferrari')
        self.assertEqual(created_car.model, 'Testarossa')


    def test_car_create_wrong_make(self):
        url = reverse('car-list-and-create')
        data = {'make': 'DeLorean', 'model': 'DMC-12'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


    def test_car_create_correct_make_wrong_model(self):
        url = reverse('car-list-and-create')
        data = {'make': 'Porsche', 'model': 'Testarossa'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


    def test_car_create_already_exists(self):
        url = reverse('car-list-and-create')
        url = reverse('car-list-and-create')
        data = {'make': 'Porsche', 'model': '911'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


    def test_car_delete(self):
        url = reverse('car-delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Car.objects.count(), 2)


    def test_car_delete_wrong_id(self):
        url = reverse('car-delete', args=[4])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Car.objects.count(), 3)


    def test_car_rate(self):
        url = reverse('car-rate')
        data = {'car_id': 2, 'rating': 5}
        response = self.client.post(url, data)
        ratings_count = Car.objects.get(pk=2).ratings.count()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ratings_count, 3)


    def test_car_rate_wrong_id(self):
        url = reverse('car-rate')
        data = {'car_id': 4, 'rating': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)


    def test_car_rate_wrong_rating(self):
        url = reverse('car-rate')
        data1 = {'car_id': 2, 'rating': 0}
        response1 = self.client.post(url, data1)
        data2 = {'car_id': 2, 'rating': 6}
        response2 = self.client.post(url, data2)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)


    def test_popular_car_list(self):
        url = reverse('popular-car-list')
        expected_data = [
            {'id': 2, 'make': 'Aston Martin', 'model': 'Vanquish', 'rates_number': 2},
            {'id': 1, 'make': 'Porsche', 'model': '911', 'rates_number': 1},
            {'id': 3, 'make': 'Maserati', 'model': 'Quattroporte', 'rates_number': 0},
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
