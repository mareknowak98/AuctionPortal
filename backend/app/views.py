import re
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotAllowed
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, AuctionSerializer, CategorySerializer, AuctionCreateSerializer, \
    BidSerializer, BidCreateSerializer, ProfileSerializer, UserMessageSerializer
from .models import Auction, Category, Bid, Profile, UserMessage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import response, decorators, permissions, status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # print(self.request.user.id)
        return User.objects.filter(id=self.request.user.id)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AuctionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AuctionCreate(viewsets.ModelViewSet):
    """
    Create Auction - only for authenticated users.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        return Response("ok")


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        auctionID = Auction.objects.get(id=data['bidAuction'])

        userbuyerID = User.objects.get(id=request.user.id)
        newBid = Bid.objects.create(bidUserBuyer=userbuyerID,
                                    bidAuction=auctionID,
                                    bidPrice=data['bidPrice'],
                                    )
        if not request.user.is_authenticated:
            return HttpResponseNotAllowed("You must be logged!")

        if int(userbuyerID.id) == auctionID.user_seller.id:
            return HttpResponseNotAllowed("You cannot bid your own auction!")

        if str(auctionID.date_end) < str(datetime.now().strftime("%Y-%m-%d %H:%M")):
            return HttpResponseNotAllowed("This auction is overdue!")

        if auctionID.user_highest_bid is not None and auctionID.highest_bid is not None:
            if float(auctionID.highest_bid) >= float(data['bidPrice']):
                return HttpResponseNotAllowed("Bid offer have to be higher than current highest bid!")

        Auction.objects.filter(id=data['bidAuction']).update(highest_bid=data['bidPrice'])
        Auction.objects.filter(id=data['bidAuction']).update(user_highest_bid=userbuyerID.id)

        serializer = BidCreateSerializer(newBid, many=False)
        return Response(serializer.data)


class BidCreate(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.request.user.id)
        user = self.request.user
        # print(len(self.request.data) == 0)
        # if len(self.request.data) == 0:
        #     print("num 1")
        #     return Profile.objects.all()
        # data = self.request.data
        # # print(data)
        # user = data['userProfile']
        # print("num 2")
        return Profile.objects.filter(profileUser=user)

    def update(self, request, *args, **kwargs):
        print("------")
        data = request.data
        profile = self.get_object()
        userID = User.objects.get(id=profile.profileUser.id)  # check if user which send request == this profile owner
        print("req data = {}".format(request.data))
        # print("neme {}".format(data['profileUserName']))
        # print("surname {}".format(data['profileUserSurname']))
        if not request.user.is_authenticated:
            return HttpResponseNotAllowed("You must be logged!")

        # print("1 {}".format(request.user.id))
        # print("2 {}".format(userID.id))
        if request.user.id != userID.id:
            print(1)
            return HttpResponseNotAllowed("Dont try to change somebody else profile!")

        if not len(data['profileUserName']) > 0 and data['profileUserName'].isalpha() or not len(data['profileUserSurname'])>0 and data['profileUserSurname'].isalpha():
            print(2)
            return HttpResponseNotAllowed("Name and surname have to be letter strings")

        if len(data['profileNumberOfOpinions']) > 0 or len(data['profileAvgOpinion']) > 0:
            print(3)
            # print(data['profileNumberOfOpinions'] is None)
            # print(data['profileAvgOpinion'] is None)
            # print("data:" + data['profileNumberOfOpinions'] + ".")
            # print(type(data['profileAvgOpinion']))
            # print(len(data['profileAvgOpinion']))
            return HttpResponseNotAllowed("You can't do this!")

        if re.match("^[0-9 ]+$", data['profileBankAccountNr']):
            print(4)
            return HttpResponseNotAllowed("Account number may only contains digits")
        if len(data['profileUserName']) > 0:
            profile.profileUserName = data['profileUserName']
        if len(data['profileUserSurname']) > 0:
            profile.profileUserSurname = data['profileUserSurname']
        if len(data['profileBankAccountNr']) > 0:
            profile.profileBankAccountNr = data['profileBankAccountNr']
        if len(data['profileTelephoneNumber']) > 0:
            profile.profileTelephoneNumber = data['profileTelephoneNumber']
        if data['profileAvatar'] is not None and not isinstance(data['profileAvatar'], str):
            profile.profileAvatar = data['profileAvatar']

        print("correct")
        profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)


##############
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


def response_validation_error(error):
    return response.Response(error, status.HTTP_400_BAD_REQUEST)


def response_created(data):
    return response.Response(data, status.HTTP_201_CREATED)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsOwner, ])
def get_inbox_messages(request):
    user = request.user
    msgbox = UserMessage.objects.filter(usermessToUser=user)
    serializer = UserMessageSerializer(msgbox, many=True)
    return response_created(serializer.data)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsOwner, ])
def get_outbox_messages(request):
    user = request.user
    msgbox = UserMessage.objects.filter(usermessFromUser=user)
    serializer = UserMessageSerializer(msgbox, many=True)
    return response_created(serializer.data)


@decorators.api_view(["POST"])
@decorators.permission_classes([IsOwner, ])
def send_message(request):
    if request.method == 'POST':
        user = request.user

        to_user_id = request.POST.get('to_user_id')
        text = request.POST.get('text')
        if not to_user_id:
            return response_validation_error({'to_user_id': ["This field is required."]})

        if not text:
            return response_validation_error({'text': ["This field is required."]})

        if not User.objects.filter(pk=to_user_id).exists():
            return response_validation_error({'to_user_id': ["User should be exist."]})


        data = {
            'usermessFromUser': user.id,
            'usermessToUser': to_user_id,
            'usermessMessage': {
                'messageContent': request.POST.get('text')
            }
        }
        user_msg_serializer = UserMessageSerializer(data=data)
        if not user_msg_serializer.is_valid():
            return response_validation_error(user_msg_serializer.errors)

        user_msg_serializer.save()
        return response_created({'success'})