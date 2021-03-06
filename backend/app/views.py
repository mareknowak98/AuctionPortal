import datetime as dt
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotAllowed, JsonResponse
from rest_framework import viewsets, mixins
from app.serializers import UserSerializer, AuctionSerializer, CategorySerializer, AuctionCreateSerializer, \
    BidSerializer, BidCreateSerializer, ProfileSerializer, UserMessageSerializer, Profile2Serializer, MessageSerializer, \
    OpinionSerializer, ReportSerializer, UserStaffSerializer
from .models import Auction, Category, Bid, Profile, UserMessage, Message, UserOpinion, AuctionReport
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import response, decorators, permissions, status
from itertools import chain


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request is None:
            return User.objects.none()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def getUsernameById(self, request, **kwargs):
        id = self.request.query_params.get('id', None)
        user = User.objects.get(id=id)
        print(user.username)
        return Response(user.username)

    @action(detail=False, methods=['get'])
    def getUsers(self, request, **kwargs):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            users = User.objects.all()
            serializer = UserStaffSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotAllowed("Allowed only for staff members!")

    @action(detail=False, methods=['get'])
    def getPrivileges(self, request, **kwargs):
        user = self.request.user
        result = {}
        if user.is_staff:
            result["is_staff"] = True
        else:
            result["is_staff"] = False
        if user.is_superuser:
            result["is_superuser"] = True
        else:
            result["is_superuser"] = False
        return Response(result)

class CategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        flag1 = True if data['auctionIsNew'] == 'true' else False
        flag2 = True if data['auctionIsShippingAv'] == 'true' else False
        if data['auctionImage'] != 'null':
            auctionImage = data['auctionImage']
        else:
            auctionImage = 'https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608590488/media/images/default_auction_fe1wvk'

        if data['auctionDateStarted'] > data['auctionDateEnd']:
            HttpResponseNotAllowed("You cannot set ending date in the past")
        if data['auctionMinimalPrice'] != "" and data['auctionStartingPrice'] > data['auctionMinimalPrice']:
            HttpResponseNotAllowed("Starting Price must be higher than minimal price")
        if data['auctionMinimalPrice'] == "":
            min_price = data['auctionStartingPrice']
        else:
            min_price = data['auctionMinimalPrice']

        newAuction = Auction.objects.create(
            auctionUserSeller=user,
            auctionImage=auctionImage,
            auctionCategory=Category.objects.get(id=data['auctionCategory']),
            auctionProductName=data['auctionProductName'],
            auctionDescription=data['auctionDescription'],
            auctionIsNew=flag1,
            auctionDateStarted=data['auctionDateStarted'],
            auctionDateEnd=data['auctionDateEnd'],
            auctionStartingPrice=data['auctionStartingPrice'],
            auctionMinimalPrice=min_price,
            auctionIsShippingAv=flag2,
        )
        serializer = AuctionCreateSerializer(newAuction, many=False)
        return Response(serializer.data)

    # endpoint: (patch) http://127.0.0.1:8000/api/auctioncreate/88/
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        print(data)
        auction_obj = self.get_object()
        print(auction_obj)

        flag1 = True if data.get('auctionIsNew', auction_obj.auctionIsNew) == 'true' else False
        flag2 = True if data.get('auctionIsShippingAv', auction_obj.auctionIsShippingAv) == 'true' else False

        auction_obj.auctionImage = data.get('auctionImage', auction_obj.auctionImage)
        auction_obj.auctionCategory = Category.objects.get(
            id=data.get('auctionCategory', auction_obj.auctionCategory.id))
        auction_obj.auctionProductName = data.get('auctionProductName', auction_obj.auctionProductName)
        auction_obj.auctionDescription = data.get('auctionDescription', auction_obj.auctionDescription)
        auction_obj.auctionIsNew = flag1
        auction_obj.auctionIsShippingAv = flag2
        auction_obj.auctionShippingCost = data.get('auctionShippingCost', auction_obj.auctionShippingCost)

        if data.get('auctionIsShippingAv') is None and data.get('auctionShippingCost') is not None:
            return HttpResponseNotAllowed("Not allowed")
        if data.get('auctionDateEnd'):
            return HttpResponseNotAllowed("You cannot change end date of auction")
        if data.get('auctionStartingPrice') or data.get('auctionMinimalPrice'):
            return HttpResponseNotAllowed("You cannot this")
        if data.get('auctionHighestBid') or data.get('auctionUserHighestBid') or data.get(
                'auctionDateStarted') or data.get(
                'auctionUserSeller') or data.get('auctionIsActive'):
            return HttpResponseNotAllowed("You are not alleowed to change this params")

        auction_obj.save()
        serializer = AuctionCreateSerializer(auction_obj, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        auction_obj = self.get_object()
        if user == auction_obj.auctionUserSeller:
            return super(AuctionViewSet, self).destroy(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed("You are not allowed to delete not your auctions")

    def list(self, request, *args, **kwargs):
        auctions = Auction.objects.all().filter(auctionIsActive=True)
        title = self.request.query_params.get('title', None)
        desc = self.request.query_params.get('desc', None)  # auctionDescription
        cat = self.request.query_params.get('cat', None)  # category (id)
        min = self.request.query_params.get('min', None)  # min price
        max = self.request.query_params.get('max', None)  # min price
        time_left = self.request.query_params.get('time_left',
                                                  None)  # 1 ascending(shortest time), 2 descending(longest time), none without sorting
        new = self.request.query_params.get('new', None)
        ship = self.request.query_params.get('ship', None)  # shipping
        price = self.request.query_params.get('price',
                                              None)  # 1 ascending(min price -> max price), 2 descending, none without sorting
        if title:
            auctions = auctions.filter(auctionProductName__icontains=title)
        if desc:
            auctions = Auction.objects.all().filter(auctionProductName__icontains=title) | Auction.objects.all().filter(
                auctionDescription__icontains=desc, auctionIsActive=True)
        if cat:
            auctions = auctions.filter(auctionCategory=Category.objects.get(id=cat))
        if min:
            auctions = auctions.filter(auctionHighestBid__gte=min)
        if max:
            auctions = auctions.filter(auctionHighestBid__lte=max)
        if new:
            auctions = auctions.filter(auctionIsNew=new)
        if ship:
            auctions = auctions.filter(auctionIsShippingAv=ship)
        if time_left and int(time_left) == 1:
            auctions = auctions.order_by('auctionDateEnd')
        if time_left and int(time_left) == 2:
            auctions = auctions.order_by('-auctionDateEnd')
        if price and int(price) == 1:
            auctions = auctions.order_by('auctionHighestBid')
        if price and int(price) == 2:
            auctions = auctions.order_by('-auctionHighestBid')
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data)

    # http://127.0.0.1:8000/api/auctions/getMyAuctions/?active=True&ended=False
    @action(detail=False, methods=['get'])
    def getMyAuctions(self, request, **kwargs):
        auctionIsActive = self.request.query_params.get('active', None)
        is_ended = self.request.query_params.get('ended', None)
        user = request.user
        if auctionIsActive == 'True':
            myAuctions = Auction.objects.filter(auctionUserSeller=user, auctionIsActive=auctionIsActive)
        if auctionIsActive == 'False' and is_ended == 'True':
            myAuctions = Auction.objects.filter(auctionUserSeller=user, auctionIsActive=auctionIsActive,
                                                auctionUserHighestBid__isnull=False)
        if auctionIsActive == 'False' and is_ended == 'False':
            myAuctions = Auction.objects.filter(auctionUserSeller=user, auctionIsActive=auctionIsActive,
                                                auctionUserHighestBid__isnull=True)
        if auctionIsActive == 'False' and is_ended == None:
            myAuctions = Auction.objects.filter(auctionUserSeller=user, auctionIsActive=auctionIsActive)

        serializer = AuctionSerializer(myAuctions, many=True)
        return Response(serializer.data)

    # params:
    # active - boolean, determine the output to active/ended auctions
    # endpoint: http://127.0.0.1:8000/api/auctions/getMyParticipatedAuctions/?active=True
    @action(detail=False, methods=['get'])
    def getMyParticipatedAuctions(self, request, **kwargs):
        auctionIsActive = self.request.query_params.get('active', None)
        user = request.user
        bids = Bid.objects.filter(bidUserBuyer=user)
        auctions_queryset = Auction.objects.filter(id__in=bids.values_list('bidAuction', flat=False),
                                                   auctionIsActive=auctionIsActive)
        serializer = AuctionSerializer(auctions_queryset, many=True)
        return Response(serializer.data)

    # endpoint: http://127.0.0.1:8000/api/auctions/getMyWonAuctions
    @action(detail=False, methods=['get'])
    def getMyWonAuctions(self, request, **kwargs):
        user = request.user
        auctions_queryset = Auction.objects.filter(auctionUserHighestBid=user.id, auctionIsActive=False)
        serializer = AuctionSerializer(auctions_queryset, many=True)
        return Response(serializer.data)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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

        if int(userbuyerID.id) == auctionID.auctionUserSeller.id:
            return HttpResponseNotAllowed("You cannot bid your own auction!")

        if str(auctionID.auctionDateEnd) < str(datetime.now().strftime("%Y-%m-%d %H:%M")):
            return HttpResponseNotAllowed("This auction is overdue!")

        if auctionID.auctionUserHighestBid is not None and auctionID.auctionHighestBid is not None:
            if float(auctionID.auctionHighestBid) >= float(data['bidPrice']):
                return HttpResponseNotAllowed("Bid offer have to be higher than current highest bid!")

        Auction.objects.filter(id=data['bidAuction']).update(auctionHighestBid=data['bidPrice'])
        Auction.objects.filter(id=data['bidAuction']).update(auctionUserHighestBid=userbuyerID.id)

        serializer = BidCreateSerializer(newBid, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def getAuctionBids(self, request, **kwargs):
        auction_id = self.request.query_params.get('auction_id', None)
        bids = reversed(Bid.objects.filter(bidAuction=auction_id))
        serializer = BidCreateSerializer(bids, many=True)
        return Response(serializer.data)


# class BidCreate(viewsets.ModelViewSet):
#     queryset = Bid.objects.all()
#     serializer_class = BidCreateSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.request is None:
            return Profile.objects.none()
        user = self.request.user
        return Profile.objects.filter(profileUser=user)

    def update(self, request, *args, **kwargs):
        print("------")
        data = request.data
        profile = self.get_object()
        userID = User.objects.get(id=profile.profileUser.id)  # check if user which send request == this profile owner
        if not request.user.is_authenticated:
            return HttpResponseNotAllowed("You must be logged!")

        if request.user.id != userID.id:
            return HttpResponseNotAllowed("Dont try to change somebody else profile!")

        if not len(data['profileUserName']) > 0 and data['profileUserName'].isalpha() or not len(
                data['profileUserSurname']) > 0 and data['profileUserSurname'].isalpha():
            return HttpResponseNotAllowed("Name and surname have to be letter strings")

        if len(data['profileUserName']) > 0:
            profile.profileUserName = data['profileUserName']
        if len(data['profileUserSurname']) > 0:
            profile.profileUserSurname = data['profileUserSurname']
        if len(data['profileTelephoneNumber']) > 0:
            profile.profileTelephoneNumber = data['profileTelephoneNumber']
        if data['profileAvatar'] is not None and not isinstance(data['profileAvatar'], str):
            profile.profileAvatar = data['profileAvatar']

        profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    # endpoint http://127.0.0.1:8000/api/profile/getUserIdByProfile?profile_id=5
    @action(detail=False, methods=['GET'])
    def getUserIdByProfile(self, request, **kwargs):
        profile_id = request.GET.get('profile_id')
        profile_get = Profile.objects.get(id=profile_id[0])
        user = User.objects.filter(profile=profile_get).first()
        return Response(user.id)


##############
class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = Profile2Serializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def getMyProfile(self, request, **kwargs):
        user = request.user
        profile = Profile.objects.get(profileUser=user)
        serializer = Profile2Serializer(profile)
        return Response(serializer.data);

    # endpoint http://127.0.0.1:8000/api/profileUser/getProfileByUserId?id=2
    @action(detail=False, methods=['GET'])
    def getProfileByUserId(self, request, **kwargs):
        user_id = request.GET.get('id')
        print(user_id)
        profile = Profile.objects.get(profileUser=User.objects.get(id=user_id))
        serializer = Profile2Serializer(profile)
        return Response(serializer.data);

    # endpoint http://127.0.0.1:8000/api/profileUser/getUserImage?user_id=20
    @action(detail=False, methods=['GET'])
    def getUserImage(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        profile = Profile.objects.get(profileUser=User.objects.get(id=user_id))
        serializer = Profile2Serializer(profile)
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


@decorators.api_view(["POST"])
def get_user_profile_by_auction_id(request):
    if request.method == 'POST':
        auctionId = request.POST.get('id')
        auction = Auction.objects.get(id=auctionId)
        userID = User.objects.get(id=auction.auctionUserSeller.id)
        userProfileID = Profile.objects.get(profileUser=userID)
        return response_created({userProfileID.id})


# return all users with messages with request user

@decorators.api_view(["GET"])
def get_messages_user_list(request):
    if request.method == 'GET':
        user = request.user
        messages = UserMessage.objects.filter(usermessFromUser=user).values('usermessToUser__id',
                                                                            'usermessToUser__username').distinct()
        print(messages)
        messages2 = UserMessage.objects.filter(usermessToUser=user).values('usermessFromUser_id',
                                                                           'usermessFromUser__username').distinct()
        print(messages2)
        # messages.union(messages2)
        # print(messages)
        return response_created(list(chain(messages, messages2)))


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    '''
    returns send and received messages with selected user params:
    userToID - user to check messages with
    endpoint: http://127.0.0.1:8000/api/messages/getMessagesWithUser/
    '''

    @action(detail=False, methods=['post'])
    def getMessagesWithUser(self, request, **kwargs):
        user = request.user
        data = request.data
        send_user_messages = UserMessage.objects.filter(usermessFromUser=user.id, usermessToUser=data['userToID'])
        send_messages = Message.objects.filter(id__in=send_user_messages.values_list('usermessMessage', flat=False))
        received_user_messages = UserMessage.objects.filter(usermessToUser=user.id, usermessFromUser=data['userToID'])
        received_messages = Message.objects.filter(
            id__in=received_user_messages.values_list('usermessMessage', flat=False))
        return Response({'from': MessageSerializer(send_messages, many=True).data,
                         "to": MessageSerializer(received_messages, many=True).data})


class OpinionViewSet(viewsets.ModelViewSet):
    queryset = UserOpinion.objects.all()
    serializer_class = OpinionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = request.data
        if request.user == data['opinionUserAbout']:
            return HttpResponseNotAllowed("You cant write opinion about yourself!")
        if int(data['opinionStars']) > 5 or int(data['opinionStars']) < 1:
            return HttpResponseNotAllowed("1-5 rating scale")
        newOpinion = UserOpinion.objects.create(
            opinionUserAuthor=request.user,
            opinionUserAbout=User.objects.get(id=data['opinionUserAbout']),
            opinionDescription=data['opinionDescription'],
            opinionStars=data['opinionStars'],
        )

        serializer = OpinionSerializer(newOpinion, many=False)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        opinion_obj = self.get_object()
        if int(data.get('opinionStars')) > 5 or int(data.get('opinionStars')) < 1:
            return HttpResponseNotAllowed("1-5 rating scale")
        opinion_obj.opinionDescription = data.get('opinionDescription', opinion_obj.opinionDescription)
        opinion_obj.opinionStars = data.get('opinionStars', opinion_obj.opinionStars)
        # tz = pytz.timezone('Poland')
        opinion_obj.opinionDate = datetime.now() + dt.timedelta(hours=1)
        opinion_obj.save()
        serializer = OpinionSerializer(opinion_obj, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        opinion_obj = self.get_object()
        if user == opinion_obj.opinionUserAuthor:
            return super(OpinionViewSet, self).destroy(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed("You are not alleowed to delete not your opinions")

    # endpoint: http://127.0.0.1:8000/api/opinion/getUserOpinions?user_id=20
    @action(detail=False, methods=['get'])
    def getUserOpinions(self, request, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        try:
            user = User.objects.get(id=user_id)
            user_opinion = UserOpinion.objects.filter(opinionUserAbout=user)
            serializer = OpinionSerializer(user_opinion, many=True)
            return Response(serializer.data)
        except:
            return Response("no such user")

    # endpoint: http://127.0.0.1:8000/api/opinion/getUserAvgRating?user_id=20
    @action(detail=False, methods=['get'])
    def getUserAvgRating(self, request, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        try:
            user = User.objects.get(id=user_id)
            user_opinion = UserOpinion.objects.filter(opinionUserAbout=user)
            ratings = list(user_opinion.values("opinionStars"))
            result = float(sum(d['opinionStars'] for d in ratings)) / len(ratings)
            return Response(result)
        except:
            return Response("no such user")


class ReportViewSet(viewsets.ModelViewSet):
    queryset = AuctionReport.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        report_content = data.get('reportContent', 'No description available.')
        try:
            auction = Auction.objects.get(id=data.get('reportAuction'))
            newReport = AuctionReport.objects.create(
                reportAuction=auction,
                reportUser=user,
                reportContent=report_content,
            )
            serializer = ReportSerializer(newReport, many=False)
            return Response(serializer.data)
        except AssertionError:
            return Response("Error")
        except:
            return Response("no such user or auction")

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super(ReportViewSet, self).destroy(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed("Only allowed for staff and superusers")

    @action(detail=False, methods=['get'])
    def getReports(self, request, **kwargs):
        user = request.user
        print(user)
        if user.is_staff or user.is_superuser:
            reports_queryset = AuctionReport.objects.all()
            serializer = ReportSerializer(reports_queryset, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotAllowed("Only allowed for staff and superusers")


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # endpoint: http://127.0.0.1:8000/api/staff/isStaffUser?user_id=23
    @action(detail=False, methods=['get'])
    def isStaffUser(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        user = User.objects.get(id=user_id)
        if user.is_staff or user.is_superuser:
            return Response("True")
        else:
            return Response("False")

    # endpoint: http://127.0.0.1:8000/api/staff/grantStaffStatus/
    @action(detail=False, methods=['post'])
    def grantStaffStatus(self, request, *args, **kwargs):
        data = request.data
        user_request = request.user
        user_id = data.get('user_id')
        if user_request.is_staff or user_request.is_superuser:
            user_grant_status = User.objects.get(id=user_id)
            user_grant_status.is_staff = True
            user_grant_status.save()
            return Response("ok")
        else:
            return HttpResponseNotAllowed("Allowed only for staff members!")

    # endpoint: http://127.0.0.1:8000/api/staff/revokeStaffStatus/
    @action(detail=False, methods=['post'])
    def revokeStaffStatus(self, request, *args, **kwargs):
        data = request.data
        user_request = request.user
        user_id = data.get('user_id')
        if user_request.is_staff or user_request.is_superuser:
            user_revoke_status = User.objects.get(id=user_id)
            user_revoke_status.is_staff = False
            user_revoke_status.save()
            return Response("ok")
        else:
            return HttpResponseNotAllowed("Allowed only for staff members!")

    # endpoint: http://127.0.0.1:8000/api/staff/setActivateUser/
    @action(detail=False, methods=['post'])
    def setActivateUser(self, request, *args, **kwargs):
        data = request.data
        user_request = request.user
        ban_unban = data.get('ban')
        ban = ban_unban == 'True'
        user_id = data.get('user_id')
        if user_request.is_staff or user_request.is_superuser:
            try:
                user_to_delete = User.objects.get(id=user_id)
                if user_to_delete.is_staff or user_to_delete.is_superuser:
                    return HttpResponseNotAllowed("Not allowed")
                user_to_delete.is_active = not ban
                user_to_delete.save()
                return Response("ok")
            except User.DoesNotExist:
                return Response("No such user")
            except Exception as e:
                return Response({'err': e.message})
        else:
            return HttpResponseNotAllowed("Allowed only for staff members!")

    # endpoint: http://127.0.0.1:8000/api/staff/deleteAuction/
    @action(detail=False, methods=['post'])
    def deleteAuction(self, request, *args, **kwargs):
        data = request.data
        user_request = request.user
        auction_id = data.get('auction_id')
        if user_request.is_staff or user_request.is_superuser:
            try:
                auction_to_delete = Auction.objects.get(id=auction_id)
                auction_to_delete.delete()
                return Response("ok")
            except Auction.DoesNotExist:
                return Response("No such auction")
            except Exception as e:
                return Response({'err': e.message})
        else:
            return HttpResponseNotAllowed("Allowed only for staff members!")
