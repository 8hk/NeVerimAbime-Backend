from django.test import TestCase

# Create your tests here.
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import User


class NutrientTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             name="testuser",
                                             password="pass123testuser",
                                             email='user@foo.com')
        self.user.is_active = True
        self.user.save()
        response = self.client.post("/api/v1/auth/token/", {"username": "testuser", "password": "pass123testuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "The token should be successfully returned.")
        response_content = json.loads(response.content.decode('utf-8'))
        self.token = response_content["access"]
        self.api_auth()

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_nutrient_create(self):
        data = {
            "name": "dummy nutrient",
            "unitName": "dummy unit name",
            "ingredientId": "12345",
            "fdcId": "78912",
            "fdcNumber": "827391",
            "fdcRank": "9",
            "amount": "122"
        }

        response = self.client.post("/api/nutrient/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
