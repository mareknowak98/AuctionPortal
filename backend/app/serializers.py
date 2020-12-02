from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Auction, Category, Bid
from rest_framework.authentication import TokenAuthentication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if email == '':
            raise serializers.ValidationError("Enter an email")
        if not username.isalnum():
            raise serializers.ValidationError("Username should oly contain alphanumeric characters")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']
        # fields = ['category_name',]


class AuctionSerializer(serializers.ModelSerializer):
    user_seller = UserSerializer(many=False)
    # product = ProductSerializer(many=False)
    category = CategorySerializer(many=False)
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Auction
        fields = ['id', 'category','image', 'product_name', 'description', 'is_new', 'user_seller', 'user_highest_bid', 'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av', 'is_active']


class AuctionCreateSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())
    user_seller = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Auction
        fields = ['id', 'category','image', 'product_name', 'description', 'is_new', 'user_seller',  'user_highest_bid', 'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av']

class BidSerializer(serializers.ModelSerializer):
    bidUserBuyer = UserSerializer(many=False)
    bidAuction = AuctionSerializer(many=False)
    class Meta:
        model = Bid
        fields = ['id', 'bidUserBuyer', 'bidAuction', 'bidPrice', 'bidDate']

class BidCreateSerializer(serializers.ModelSerializer):
    bidUserBuyer = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    bidAuction = serializers.PrimaryKeyRelatedField(many=False, queryset=Auction.objects.all())
    class Meta:
        model = Bid
        fields = ['id', 'bidUserBuyer', 'bidAuction', 'bidPrice', 'bidDate']