from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Auction, Category
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

class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False)
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    category = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'category','image', 'product_name', 'description', 'is_new']

class AuctionSerializer(serializers.ModelSerializer):
    user_seller = UserSerializer(many=False)
    product = ProductSerializer(many=False)

    product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())
    user_seller = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    class Meta:
        model = Auction
        fields = ['id', 'user_seller', 'product', 'user_highest_bid', 'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av']


    # def create(self, validated_data):
    #     product_data = validated_data.pop('product')
    #     product_tag, created = Product.objects.get_or_create(id=product_data)
    #     auction_instance = Auction.objects.create(**validated_data, product=product_tag)

# class AuctionSerializer(serializers.ModelSerializer):
#     # user_seller = UserSerializer(many=False)
#     # product = ProductSerializer(many=False)
#
#     class Meta:
#         model = Auction
#         fields = ['id', 'user_seller', 'product', 'user_highest_bid', 'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av']
#
#     def get(self):
#         user_seller = UserSerializer(many=False)
#         product = ProductSerializer(many=False)
#
#     def create(self, validated_data):
#         product_data = validated_data.pop('product')
#         product = ProductSerializer.create(ProductSerializer(), validated_data=product_data)
#         auction = Auction.objects.update_or_create(product=product)
#         return auction