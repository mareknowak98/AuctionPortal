from django.conf.urls import url, include
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'filmy', views.FilmViewSet, basename="film")
# router.register(r'recenzje', views.RecenzjeViewSet, basename="recenzje")
# router.register(r'aktorzy', views.AktorViewSet, basename="aktorzy")

urlpatterns = [
    url(r'^', include(router.urls))
]