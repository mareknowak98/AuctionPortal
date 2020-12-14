import re
import datetime as dt
from datetime import datetime
import pytz
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotAllowed, JsonResponse
from rest_framework import viewsets, mixins
from app.serializers import UserSerializer, AuctionSerializer, CategorySerializer, AuctionCreateSerializer, \
    BidSerializer, BidCreateSerializer, ProfileSerializer, UserMessageSerializer, Profile2Serializer, MessageSerializer, \
    OpinionSerializer, ReportSerializer
from .models import Auction, Category, Bid, Profile, UserMessage, Message, UserOpinion, AuctionReport
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import response, decorators, permissions, status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def getUsernameById(self, request, **kwargs):
        id = self.request.query_params.get('id', None)
        user = User.objects.get(id=id)
        print(user.username)
        return Response(user.username)




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
    # search_fields = ('product_name', 'description')

    def list(self, request, *args, **kwargs):
        params = request.GET
        print(list(params.values()))
        auctions = Auction.objects.all().filter(is_active=True)
        title = self.request.query_params.get('title', None)
        desc = self.request.query_params.get('desc', None) #description
        cat = self.request.query_params.get('cat', None) #category (id)
        min = self.request.query_params.get('min', None) #min price
        max = self.request.query_params.get('max', None) #min price
        time_left = self.request.query_params.get('time_left', None) #1 ascending(shortest time), 2 descending(longest time), none without sorting
        new = self.request.query_params.get('new', None)
        ship = self.request.query_params.get('ship', None) #shipping
        price = self.request.query_params.get('price', None) #1 ascending(min price -> max price), 2 descending, none without sorting
        ##TODO remove prints and reparin price ordering
        if title:
            print(1)
            auctions = auctions.filter(product_name__icontains=title)
        if desc:
            print(2)
            auctions = Auction.objects.all().filter(product_name__icontains=title) | Auction.objects.all().filter(description__icontains=desc, is_active=True)
        if cat:
            print(3)
            auctions = auctions.filter(category=Category.objects.get(id=cat))
        if min:
            print(4)
            auctions = auctions.filter(highest_bid__gte=min)
        if max:
            print(5)
            auctions = auctions.filter(highest_bid__lte=max)
        if new:
            print(6)
            auctions = auctions.filter(is_new=new)
        if ship:
            print(7)
            auctions = auctions.filter(is_shipping_av=ship)
        if time_left and int(time_left) == 1:
            print(8)
            auctions = auctions.order_by('date_end')
        if time_left and int(time_left) == 2:
            print(9)
            auctions = auctions.order_by('-date_end')
        if price and int(price) == 1:
            print(10)
            auctions = auctions.order_by('highest_bid')
        if price and int(price) == 2:
            print(11)
            auctions = auctions.order_by('-highest_bid')
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data)

    ##TODO to fix
    # params:
    # active - boolean, determine the output to active/ended auctions
    # http://127.0.0.1:8000/api/auctions/getMyAuctions/?active=True&ended=False
    @action(detail=False, methods=['get'])
    def getMyAuctions(self, request, **kwargs):
        is_active = self.request.query_params.get('active', None)
        is_ended = self.request.query_params.get('ended', None)
        user = request.user
        if is_active and not is_ended:
            Auction.objects.filter(user_seller=user, is_active=is_active)
        else:
            myAuctions = Auction.objects.filter(user_seller=user, is_active=is_active)
        serializer = AuctionSerializer(myAuctions, many=True)
        return Response(serializer.data)

    # params:
    # active - boolean, determine the output to active/ended auctions
    # endpoint: http://127.0.0.1:8000/api/auctions/getMyParticipatedAuctions/?active=True
    @action(detail=False, methods=['get'])
    def getMyParticipatedAuctions(self, request, **kwargs):
        is_active = self.request.query_params.get('active', None)
        user = request.user
        bids = Bid.objects.filter(bidUserBuyer=user)
        auctions_queryset = Auction.objects.filter(id__in=bids.values_list('bidAuction', flat=False),
                                                   is_active=is_active)
        serializer = AuctionSerializer(auctions_queryset, many=True)
        return Response(serializer.data)

    # endpoint: http://127.0.0.1:8000/api/auctions/getMyWinAuctions
    @action(detail=False, methods=['get'])
    def getMyWonAuctions(self, request, **kwargs):
        user = request.user
        print(user)
        auctions_queryset = Auction.objects.filter(user_highest_bid=user.id, is_active=False)
        serializer = AuctionSerializer(auctions_queryset, many=True)
        return Response(serializer.data)

    ##TODO find and check hishest_bid parameter in case on ending auction


class AuctionCreate(viewsets.ModelViewSet):
    """
    Create Auction - only for authenticated users.
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        # print(data)
        flag1 = True if data['is_new'] == 'true' else False
        flag2 = True if data['is_shipping_av'] == 'true' else False
        if data['image'] != 'null':
            image = data['image']
        else:
            image = '/default_auction.jpg'

        if data['date_started'] > data['date_end']:
            HttpResponseNotAllowed("You cannot set ending date in the past")
        if data['minimal_price'] != "" and data['starting_price'] > data['minimal_price']:
            HttpResponseNotAllowed("Starting Price must be higher than minimal price")
        if data['minimal_price'] == "":
            min_price = data['starting_price']
        else:
            min_price = data['minimal_price']

        newAuction = Auction.objects.create(
            user_seller=user,
            image=image,
            category=Category.objects.get(id=data['category']),
            product_name=data['product_name'],
            description=data['description'],
            is_new=flag1,
            date_started=data['date_started'],
            date_end=data['date_end'],
            starting_price=data['starting_price'],
            minimal_price=min_price,
            is_shipping_av=flag2,
        )
        serializer = AuctionCreateSerializer(newAuction, many=False)
        return Response(serializer.data)

    # endpoint: (patch) http://127.0.0.1:8000/api/auctioncreate/88/
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        auction_obj = self.get_object()
        auction_obj.image = data.get('image', auction_obj.image)
        auction_obj.category = Category.objects.get(id=data.get('category', auction_obj.category.id))
        auction_obj.product_name = data.get('product_name', auction_obj.product_name)
        auction_obj.description = data.get('description', auction_obj.description)
        auction_obj.is_new = data.get('auction_obj', auction_obj.is_new)
        auction_obj.is_shipping_av = data.get('is_shipping_av', auction_obj.is_shipping_av)

        if data.get('date_end'):
            return HttpResponseNotAllowed("You cannot change end date of auction")
        if data.get('starting_price') or data.get('minimal_price'):
            return HttpResponseNotAllowed("You cannot this")
        if data.get('highest_bid') or data.get('user_highest_bid') or data.get('date_started') or data.get(
                'user_seller') or data.get('is_active'):
            return HttpResponseNotAllowed("You are not alleowed to change this params")

        auction_obj.save()
        serializer = AuctionCreateSerializer(auction_obj, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        auction_obj = self.get_object()
        if user == auction_obj.user_seller:
            return super(AuctionCreate, self).destroy(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed("You are not alleowed to delete not your auctions")


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

    # def retrieve(self, request, *args, **kwargs):
    #     data = request.data
    #     print(data)

    def get_queryset(self):
        print(self.request.user.id)
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

        if re.match("^[0-9 ]+$", data['profileBankAccountNr']):
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

        profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    #endpoint http://127.0.0.1:8000/api/profile/getUserIdByProfile?profile_id=5
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

    #endpoint http://127.0.0.1:8000/api/profileUser/getProfileByUserId?id=2
    @action(detail=False, methods=['GET'])
    def getProfileByUserId(self, request, **kwargs):
        user_id = request.GET.get('id')
        print(user_id)
        profile = Profile.objects.get(profileUser=User.objects.get(id=user_id))
        serializer = Profile2Serializer(profile)
        return Response(serializer.data);

    #endpoint http://127.0.0.1:8000/api/profileUser/getUserImage?user_id=20
    @action(detail=False, methods=['GET'])
    def getUserImage(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        profile = Profile.objects.get(profileUser=User.objects.get(id=user_id))
        serializer = Profile2Serializer(profile)
        return Response(serializer.data['profileAvatar'])

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
        userID = User.objects.get(id=auction.user_seller.id)
        userProfileID = Profile.objects.get(profileUser=userID)
        return response_created({userProfileID.id})


# return all users with messages with request user
@decorators.api_view(["GET"])
def get_messages_user_list(request):
    if request.method == 'GET':
        user = request.user
        messages = UserMessage.objects.filter(usermessFromUser=user).values('usermessToUser__id',
                                                                            'usermessToUser__username').distinct()
        messages2 = UserMessage.objects.filter(usermessToUser=user).values('usermessFromUser_id',
                                                                           'usermessFromUser__username').distinct()
        messages.union(messages2)
        return response_created(messages)


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
        tz = pytz.timezone('Poland')  # -1 hour idk why
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

    # endpoint: http://127.0.0.1:8000/api/staff/deleteUser/
    @action(detail=False, methods=['post'])
    def deleteUser(self, request, *args, **kwargs):
        data = request.data
        user_request = request.user
        user_id = data.get('user_id')
        if user_request.is_staff or user_request.is_superuser:
            try:
                user_to_delete = User.objects.get(id=user_id)
                if user_to_delete.is_staff or user_to_delete.is_superuser:
                    return HttpResponseNotAllowed("Not allowed")
                user_to_delete.delete()
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
