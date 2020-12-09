from django.conf.urls import url, include
from rest_framework import routers
from app import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'categories', views.CategoryViewSet, basename="categories")
router.register(r'auctions', views.AuctionViewSet, basename="auctions")
router.register(r'auctioncreate', views.AuctionCreate, basename="auction-create")
router.register(r'bids', views.BidViewSet, basename="bids")
router.register(r'makebid', views.BidCreate, basename="makebid")
router.register(r'profile', views.ProfileViewSet, basename="profile")
router.register(r'user-id', views.UserViewSet, basename="UserId")
router.register(r'profileUser', views.ProfileUserViewSet, basename="profileUser")
router.register(r'messages', views.MessageViewset, basename="messages")
router.register(r'opinion', views.OpinionViewSet, basename="opinion")


urlpatterns = [
    path(r'messaging/get-inbox/', views.get_inbox_messages, name='get_inbox'),
    path(r'messaging/get-outbox/', views.get_outbox_messages, name='get_outbox'),
    path(r'messaging/send/', views.send_message, name='send'),
    path(r'get_user_profile_by_auction_id/', views.get_user_profile_by_auction_id, name='get_user_profile_by_auction_id'),
    path(r'get_messages_user_list/', views.get_messages_user_list, name='get_messages_user_list'),
    url(r'^', include(router.urls)),
]