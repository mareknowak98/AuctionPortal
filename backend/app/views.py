from datetime import datetime

from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotAllowed
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, AuctionSerializer, CategorySerializer, AuctionCreateSerializer, BidSerializer, BidCreateSerializer
from .models import Auction, Category, Bid
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AuctionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

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



