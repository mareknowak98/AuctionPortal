import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
import app.models as Mod
import app.serializers as Serial
import app.views as View

class RegistrationTestCase(APITestCase):
    def test_register(self):
        data = {"username": "testCaseUser", "email": "testingmail@gmail.com", "password": "testingStrongPassword"}
        response = self.client.post("/api/users/", data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {"username": "testCaseUser", "email": "testingmail@gmail.com", "password": "testingStrongPassword"}
        response = self.client.post("/api/users/", data)
        data = {"username": "testCaseUser", "password": "testingStrongPassword"}
        response = self.client.post("/api-token-auth/", data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)