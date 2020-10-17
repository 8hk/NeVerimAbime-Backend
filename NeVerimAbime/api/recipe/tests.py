from django.test import TestCase

# Create your tests here.

from django.test import TestCase

# Create your tests here.
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import User
from api.recipe.models import Recipe


class RecipeTestCase(APITestCase):

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
        self.create_dummy_recipe()
        self.api_auth()

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

    def test_recipe_item_create(self):
        data = {
            "name": "dummy recipe",
            "preparation": "dummy recipe preparation",
            "cuisine": "dummy recipe cuisine",
            "totalCalories": 122,
            "difficulty": "Medium",
            "prep_time": "45",
            "ingredients": [{
                "name": "dummy meal ingredient",
                "energy": 12,
                "unitType": "gr",
                "recipeUuid": str(self.recipe.uuid),
                "fdcID": 789099,
                "quantity": "1222",
            },
                {
                    "name": "dummy meal ingredient",
                    "energy": 12,
                    "unitType": "gr",
                    "recipeUuid": str(self.recipe.uuid),
                    "fdcID": 789099,
                    "quantity": "1222",
                }],
            "tags": ["dummytag1","dummytag2"]
        }
        response = self.client.post("/api/recipe/", json.dumps(data),
                                content_type="application/json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_recipes(self):
        response = self.client.get("/api/recipe/getrecipes/",
                                   {"id": self.user.id})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_recipe(self):
        response = self.client.get("/api/recipe/getrecipe/",
                                   {"uuid": str(self.recipe.uuid)})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_get_portions(self):
        response = self.client.get("/api/recipe/getportions/",
                                   {"fdcId": "789099",
                                    "searchNutrient":"flour"})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cusines(self):
        response = self.client.get("/api/recipe/getcusines/")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_search(self):
        response = self.client.get("/api/recipe/search/",
                                   {"query": "flour"}
                                   )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_increase_like(self):
        response = self.client.get("/api/recipe/increaselike/",
                                   {
                                       "userId": str(self.user.id),
                                       "recipeid": str(self.recipe.uuid)
                                    }
                                   )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_following_recipes(self):
        response = self.client.get("/api/recipe/getfollowingrecipes/",
                                   {"id": str(self.user.id)}
                                   )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_recipes(self):
        response = self.client.get("/api/recipe/getallrecipes/")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)