from django.test import TestCase

# Create your tests here.
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import User
from api.nutrient.models import Nutrient
from api.recipe.models import Recipe

class MealItemTestCase(APITestCase):
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
        self.create_dummy_recipe()

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def create_dummy_recipe(self):
        self.recipe = Recipe.objects.create(name="dummyrecipe",
                                            preparation="dummy prep details",
                                            user=self.user,
                                            cuisine="dummy cuisine",
                                            calories="1200",
                                            difficulty="Medium",
                                            prep_time="35")
        self.recipe.save()

    def test_meal_item_create(self):
        data = {
            "name": "dummy meal item",
            "description": "dummy meal item description",
            "recipe": self.recipe.uuid,
            "amount": "122",
            "price": "1222",
            "meal_item_owner": self.user.pk,
        }
        response = self.client.post("/api/mealitem/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
