from django.urls import path
from . import views
from .viewsets import RoomViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", viewset=RoomViewSet, basename="rooms")

app_name = "rooms"

urlpatterns = router.urls
