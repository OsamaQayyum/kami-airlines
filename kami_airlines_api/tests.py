# kami_airlines_api/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Airplane

class AirplaneListCreateViewTestCase(TestCase):
    def setUp(self):
        # Create 2 airplanes for testing
        self.airplane1 = Airplane.objects.create(id=1, passenger_count=50)
        self.airplane2 = Airplane.objects.create(id=2, passenger_count=30)

        # API client for making requests
        self.client = APIClient()

    def test_list_airplanes(self):
        # Test GET request to retrieve the list of airplanes
        response = self.client.get('/api/airplanes/')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected keys
        self.assertIn('planeIdWithConsumption', response.data)
        self.assertIn('total_consumption_per_minute1', response.data)
        self.assertIn('max_minutes_fly', response.data)

        # Check the structure and values of the response
        self.assertEqual(len(response.data['planeIdWithConsumption']), 2)
        self.assertAlmostEqual(response.data['total_consumption_per_minute1'], 1.7145177444479562, places=6)
        self.assertAlmostEqual(response.data['max_minutes_fly'], 116.650877862099, places=6)

    def test_create_airplane(self):
        # Test POST request to create a new airplane
        data = {'id': 3, 'passenger_count': 20}
        response = self.client.post('/api/airplanes/', data, format='json')
        self.assertEqual(response.status_code, 201)

        # Check if the new airplane is created
        self.assertEqual(Airplane.objects.count(), 3)
        new_airplane = Airplane.objects.get(id=3)
        self.assertEqual(new_airplane.passenger_count, 20)

    def test_invalid_airplane_data(self):
        # Test POST request with invalid data
        invalid_data = {'id': 'invalid', 'passenger_count': 'invalid'}
        response = self.client.post('/api/airplanes/', invalid_data, format='json')
        self.assertEqual(response.status_code, 400)

        # Check that the number of airplanes in the database hasn't changed
        self.assertEqual(Airplane.objects.count(), 2)

    def test_invalid_airplane_id(self):
        # Test GET request with an invalid airplane ID
        response = self.client.get('/api/airplanes/100/')
        self.assertEqual(response.status_code, 404)

    def test_list_airplanes_with_passengers(self):
        # Test GET request to retrieve the list of airplanes with passengers
        response = self.client.get('/api/airplanes/?include_passengers=true')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected keys
        self.assertIn('planeIdWithConsumption', response.data)
        self.assertIn('total_consumption_per_minute1', response.data)
        self.assertIn('max_minutes_fly', response.data)

        # Check the values of the response
        self.assertEqual(len(response.data['planeIdWithConsumption']), 2)
        self.assertEqual(response.data['total_consumption_per_minute1'], 1.7145177444479562)
        self.assertAlmostEqual(response.data['max_minutes_fly'], 116.650877862099, places=6)
