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


class IngredientTestCase(APITestCase):
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
        self.nutrient_create()
        self.create_dummy_recipe()

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def nutrient_create(self):
        self.nutrient= Nutrient.objects.create(
                    name ="dummy nutrient",
                    unitName= "dummy unit name",
                    ingredientId= "12345",
                    fdcId= "78912",
                    fdcNumber= "827391",
                    fdcRank= "9",
                    amount= "122")

    def create_dummy_recipe(self):
        self.recipe = Recipe.objects.create(name="dummyrecipe",
                                            preparation="dummy prep details",
                                            user=self.user,
                                            cuisine="dummy cuisine",
                                            calories="1200",
                                            difficulty="Medium",
                                            prep_time="35")
        self.recipe.save()

    def test_ingredient_create(self):
        data = {
            "name": "dummy ingredient",
            "description": "dummy ingredient description",
            "caloriesPerUnit": "122",
            "unitType": "gr",
            "recipeUuid": self.recipe.uuid,
            "fdcID": "923577",
            "amount": "1212"
        }
        response = self.client.post("/api/ingredient/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
