from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, ProductSerializer, AuctionSerializer, CategorySerializer,AuctionCreateSerializer, ProductCreateSerializer
from .models import Product, Auction, Category
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response

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

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductCreateViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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