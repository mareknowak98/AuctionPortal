from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Auction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        fields = ['id', 'username', 'email']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )
    class Meta:
        model = Product
        fields = ['id', 'image', 'product_name', 'description', 'is_new']

class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    user_seller = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Auction
        fields = ['id', 'user_seller', 'product', 'user_highest_bid', 'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av']

