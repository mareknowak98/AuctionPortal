import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
import app.models as Mod
import app.serializers as Serial
import app.views as View
from app.serializers import UserSerializer, AuctionSerializer, CategorySerializer, AuctionCreateSerializer, \
    BidSerializer, BidCreateSerializer, ProfileSerializer, UserMessageSerializer, Profile2Serializer, MessageSerializer, \
    OpinionSerializer, ReportSerializer, UserStaffSerializer
from .models import Auction, Category, Bid, Profile, UserMessage, Message, UserOpinion, AuctionReport


class RegistrationTestCase(APITestCase):

    def test_register(self):
        data = {"username": "testCaseUser", "email": "testingmail@gmail.com", "password": "testingStrongPassword"}
        response = self.client.post("/api/users/", data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {"username": "testCaseUser2", "email": "testingmail@gmail.com", "password": "testingStrongPassword"}
        response = self.client.post("/api/users/", data)
        data = {"username": "testCaseUser2", "password": "testingStrongPassword"}
        response = self.client.post("/api-token-auth/", data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



# class UserViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="auctionTestUser", password="testingStrongPassword")
#         self.token = Token.objects.get(user=self.user)
#         self.api_authentiaction()
#
#     def api_authentiaction(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
#
#     def test_getUsernameById(self):
#         data = {"id": self.user.id}
#         response = self.client.get(reverse("users-getUsernameById"), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, "auctionTestUser")
#
#     def test_get_queryset(self):
#         response = self.client.get(reverse("users-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         tmpuser = User(**UserSerializer(response.data[0]).data)
#         self.assertEqual(tmpuser, self.user)
#
#     def test_getUsers(self):
#         self.user.is_staff=True
#         self.user.is_superuser=True
#         self.user.save()
#         response = self.client.get(reverse("users-getUsers"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.is_staff=False
#         self.user.is_superuser=False
#         self.user.save()
#         response = self.client.get(reverse("users-getUsers"))
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# class CategoriesViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="auctionTestUser", password="testingStrongPassword")
#         self.token = Token.objects.get(user=self.user)
#         self.api_authentiaction()
#
#     def api_authentiaction(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
#
#     def test_add(self):
#         response = self.client.post(reverse("categories-list"))
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class ProfileViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auctionTestUser", password="testingStrongPassword")
        self.token = Token.objects.get(user=self.user)
        self.api_authentiaction()

    def api_authentiaction(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    # def test_update_pass(self):
    #     data = {"profileUserName": "TestName", "profileUserSurname": "TestSurname", "profileTelephoneNumber": "123456789", "profileAvatar": "pathtoimg"}
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk" : self.user.id}), data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_update_fail(self):
    #     self.client.force_authenticate(user=None)
    #     data = {"profileUserName": "TestName", "profileUserSurname": "TestSurname", "profileTelephoneNumber": "123456789", "profileAvatar": "pathtoimg"}
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk" : 1}), data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_getUserIdByProfile(self):
    #     data = {"profile_id": 1}
    #     response = self.client.get(reverse("profile-getUserIdByProfile"), data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, 1)

    # profileUser
    # def test_retreive(self):
    #     data = {"profileUserName": "TestName", "profileUserSurname": "TestSurname",
    #             "profileTelephoneNumber": "123456789", "profileAvatar": "pathtoimg"}
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk": self.user.id}), data)
    #     response = self.client.get(reverse("profileUser-detail", kwargs={"pk" : 1}))
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['profileAvatar'], "https://res.cloudinary.com/dm2tx6lhe/image/upload/v1/media/https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608653722/media/images/default_d19dbf")
    #
    # def test_getMyProfile(self):
    #     data = {"profileUserName": "TestName", "profileUserSurname": "TestSurname",
    #             "profileTelephoneNumber": "123456789", "profileAvatar": "pathtoimg"}
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk": self.user.id}), data)
    #     response = self.client.get(reverse("profileUser-getMyProfile", kwargs={"pk": 1}))
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['profileAvatar'],
    #                      "https://res.cloudinary.com/dm2tx6lhe/image/upload/v1/media/https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608653722/media/images/default_d19dbf")

    # def test_getProfileByUserId(self):
    #     data = {"profileUserName": "TestName", "profileUserSurname": "TestSurname",
    #             "profileTelephoneNumber": "123456789", "profileAvatar": "pathtoimg"}
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk": self.user.id}), data)
    #     data = {"id" : self.user.id}
    #     response = self.client.get(reverse("profileUser-getProfileByUserId"), data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['profileAvatar'],
    #                          "https://res.cloudinary.com/dm2tx6lhe/image/upload/v1/media/https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608653722/media/images/default_d19dbf")


# class AuctionViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="auctionTestUser", password="testingStrongPassword")
#         self.token = Token.objects.get(user=self.user)
#         self.api_authentiaction()
#         self.test_create()
#
#     def api_authentiaction(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
#
#     def test_create(self):
#         category = Category(**{"category_name": "sth"})
#         category.save()
#         data = {
#             "auctionUserSeller": self.user,
#             "auctionImage": "imageurl",
#             "auctionCategory": category.id,
#             "auctionProductName": "TestProd",
#             "auctionDescription": "TestDescription",
#             "auctionIsNew": True,
#             "auctionUserHighestBid": '',
#             "auctionDateStarted": datetime.now(),
#             "auctionDateEnd": datetime(2025, 5, 1, 0, 0),
#             "auctionStartingPrice": 100,
#             "auctionHighestBid": "",
#             "auctionMinimalPrice": 150,
#             "auctionIsShippingAv": False,
#             "auctionIsActive": True,
#             "auctionShippingCost": "",
#         }
#         response = self.client.post(reverse("auctions-list"), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get(self):
#         response = self.client.get(reverse("auctions-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_patch(self):
#         data = {
#             "auctionImage": "newimageurl",
#             "auctionProductName": "TestProd2",
#             "auctionDescription": "TestDescription2",
#             "auctionIsNew": "false",
#             "auctionShippingCost" : 100,
#             "auctionIsShippingAv": "true",
#         }
#         response = self.client.patch(reverse("auctions-detail", kwargs={"pk": 1}), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["auctionImage"], 'https://res.cloudinary.com/dm2tx6lhe/image/upload/v1/media/newimageurl')
#         self.assertEqual(response.data["auctionProductName"], "TestProd2")
#         self.assertEqual(response.data["auctionDescription"], "TestDescription2")
#         self.assertEqual(response.data["auctionIsNew"], False)
#         self.assertEqual(response.data["auctionIsShippingAv"], True)
#
#     def test_getMyAuctions(self):
#         data = {
#             "active": "True",
#             "ended": "False",
#         }
#         response = self.client.get(reverse("auctions-getMyAuctions"), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_delete(self):
#         response = self.client.get(reverse("auctions-list"))
#         nr_auctions_before = len(response.data)
#         response = self.client.delete(reverse("auctions-detail", kwargs={"pk": 1}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         response = self.client.get(reverse("auctions-list"))
#         nr_auctions_after = len(response.data)
#         self.assertEqual(nr_auctions_before, nr_auctions_after+1)

class BidViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auctionTestUser", password="testingStrongPassword")
        category = Category(**{"category_name": "sth"})
        category.save()
        user2 = User.objects.create_user(username="auctionTestUser2", password="testingStrongPassword")
        user2.save()
        self.token = Token.objects.get(user=user2)
        self.api_authentiaction()
        data = {
            "auctionUserSeller": user2.id,
            "auctionImage": "imageurl",
            "auctionCategory": category.id,
            "auctionProductName": "TestProd",
            "auctionDescription": "TestDescription",
            "auctionIsNew": True,
            "auctionUserHighestBid": '',
            "auctionDateStarted": datetime.now(),
            "auctionDateEnd": datetime(2025, 5, 1, 0, 0),
            "auctionStartingPrice": 100,
            "auctionHighestBid": "",
            "auctionMinimalPrice": 150,
            "auctionIsShippingAv": False,
            "auctionIsActive": True,
            "auctionShippingCost": "",
        }
        response = self.client.post(reverse("auctions-list"), data)
        self.token = Token.objects.get(user=self.user)
        self.api_authentiaction()


    def api_authentiaction(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_make(self):
        data = {"bidAuction": 1, "bidPrice" : 2000}
        response = self.client.post(reverse("bids-list"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getAuctionBids(self):
        data = {"auction_id": 1}
        response = self.client.get(reverse("bids-getAuctionBids"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


