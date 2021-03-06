from django.test import TestCase

# Create your tests here.

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import User

# from django.contrib.auth.models import User

class RegisterationTestCase(APITestCase):
    def test_registeration(self):
        data = {"username":"test",
                "email":"test@passuniqe12.com",
                "password1":"passuniqe12",
                "password2":"passuniqe12",
                "foodProvider":"false"}

        response = self.client.post("/rest-auth/registration/",data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)



class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testuser",
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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)



    user_custom_list = reverse("profile-list")
    def test_profile_list_auth(self):
        response=self.client.get("/api/users/getusers/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_profile_list_un_auth(self):
        self.client.force_authenticate(user=None)
        response=self.client.get("/api/users/getusers/")
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_profile_me(self):
        response=self.client.get(reverse("me"),kwargs={"pk":1})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["username"],"testuser")



