import django
from django.test import TestCase

# Create your tests here.


import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import User
from api.recipe.models import Recipe


class CpdCreationTestCase(APITestCase):
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


        self.recipe=Recipe.objects.create(  name="dummyrecipe",
                                            preparation="dummy prep details",
                                            user=self.user,
                                            cuisine="dummy cuisine",
                                            calories="1200",
                                            difficulty="Medium",
                                            prep_time="35")
        self.recipe.save()


    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_cpd_creation(self):
        data = {"date": "2020-06-20",
                "gainedCalories": "0",
                "user": self.user,
                "recipeid":self.recipe.uuid
                }

        response = self.client.post("/api/cpd/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cpd_adding(self):
        data = {
                "user": self.user,
                "recipeid": self.recipe.uuid
                }

        response = self.client.get("/api/cpd/addintocalories/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_cpd_get_user_consumption(self):
        data = {
            "user": self.user,
        }

        response = self.client.get("/api/cpd/getuserconsumption/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


