from django.conf.urls import url, include
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet, basename="products")
router.register(r'auctions', views.AuctionViewSet, basename="auctions")
# router.register(r'aktorzy', views.AktorViewSet, basename="aktorzy")

urlpatterns = [
    url(r'^', include(router.urls))
]