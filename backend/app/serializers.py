from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.response import Response

from .models import Auction, Category, Bid, Profile, Message, UserMessage, UserOpinion, AuctionReport
from rest_framework.authentication import TokenAuthentication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'date_joined']
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



class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    profileUser = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['id', 'profileUserName', 'profileUserSurname', 'profileUser', 'profileAvatar', 'profileBankAccountNr',
                  'profileTelephoneNumber']

class Profile2Serializer(serializers.ModelSerializer):
    profileUser = UserMiniSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['id', 'profileUser', 'profileAvatar']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class AuctionSerializer(serializers.ModelSerializer):
    user_seller = UserMiniSerializer(many=False)
    category = CategorySerializer(many=False)
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Auction
        fields = ['id', 'category', 'image', 'product_name', 'description', 'is_new', 'user_seller', 'user_highest_bid',
                  'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av',
                  'is_active', 'auctionShippingCost']


class AuctionCreateSerializer(serializers.ModelSerializer):
    user_seller = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                                     queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Auction
        fields = ['id', 'category', 'image', 'product_name', 'description', 'is_new', 'user_seller', 'user_highest_bid',
                  'date_started', 'date_end', 'starting_price', 'highest_bid', 'minimal_price', 'is_shipping_av']


class BidSerializer(serializers.ModelSerializer):
    bidUserBuyer = UserSerializer(many=False)
    bidAuction = AuctionSerializer(many=False)

    class Meta:
        model = Bid
        fields = ['id', 'bidUserBuyer', 'bidAuction', 'bidPrice', 'bidDate']


class BidCreateSerializer(serializers.ModelSerializer):
    bidUserBuyer = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                                      queryset=User.objects.all())
    bidAuction = serializers.PrimaryKeyRelatedField(many=False, queryset=Auction.objects.all())

    class Meta:
        model = Bid
        fields = ['id', 'bidUserBuyer', 'bidAuction', 'bidPrice', 'bidDate']

#################
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "messageContent", "messageCreatedAt"]


class UserMessageSerializer(serializers.ModelSerializer):
    usermessMessage = MessageSerializer()
    usermessIsDeleted = serializers.BooleanField(default=False)

    class Meta:
        model = UserMessage
        fields = [
            "id",
            "usermessMessage",
            "usermessFromUser",
            "usermessToUser",
            "usermessIsDeleted"
        ]

    def create(self, validated_data):
        msg_data = validated_data.pop('usermessMessage')
        message = Message.objects.create(**msg_data)
        user_msg = UserMessage.objects.create(usermessMessage=message, **validated_data)
        return user_msg

class OpinionSerializer(serializers.ModelSerializer):
    # opinionUserAuthor = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), many=False, queryset=User.objects.all())
    opinionUserAbout = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

    opinionUserAuthor = UserMiniSerializer()
    # opinionUserAbout = UserMiniSerializer()
    class Meta:
        model = UserOpinion
        fields = ["id", 'opinionUserAuthor', 'opinionUserAbout', 'opinionDescription', 'opinionStars', 'opinionDate']

class ReportSerializer(serializers.ModelSerializer):
    reportUser = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), many=False, queryset=User.objects.all())
    reportAuction = serializers.PrimaryKeyRelatedField(many=False, queryset=Auction.objects.all())
    class Meta:
        model = AuctionReport
        fields = ["id", 'reportAuction', 'reportUser', 'reportContent']