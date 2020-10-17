from django.test import TestCase

# Create your tests here.
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.Comments.models import CommentString, Comments
from api.models import User
from api.recipe.models import Recipe


class CommentStringTestCase(APITestCase):

    def test_comment_string(self):
        self.dummy_comment_string = CommentString.objects.create(
            comments_string="This is dummy comment"
        )

        self.assertEqual(self.dummy_comment_string.comments_string,
                         "This is dummy comment")


class CommentTestCase(APITestCase):

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
        self.create_dummy_comment_string()
        self.create_dummy_comment()

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

    def create_dummy_comment_string(self):
        self.dummy_comment_string = CommentString.objects.create(
            comments_string="This is dummy comment"
        )

    def create_dummy_comment(self):
        self.comment = Comments.objects.create(
            recipe=self.recipe,
            commented_user=self.user
        )
        self.comment.comments.add(self.dummy_comment_string)
        self.comment.save()

    def test_comment_create(self):
        data = {
            "comment": self.comment,
            "recipeid": self.recipe.uuid
        }

        response = self.client.get("/api/recipe/writecomment/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
