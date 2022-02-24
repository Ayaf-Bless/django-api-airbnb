from django.shortcuts import render
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bathrooms = request.GET.get("bathrooms", None)
    bedrooms = request.GET.get("bedrooms", None)
    lat = request.Get.get("lat", None)
    lng = request.GET.get("lng", None)
    filter_kwarg = {}
    if max_price:
        filter_kwarg["price__lte"] = max_price
    if min_price:
        filter_kwarg["price__gte"] = min_price
    if beds:
        filter_kwarg["beds__lte"] = beds
    if bedrooms:
        filter_kwarg["bedrooms__lte"] = bedrooms
    if bathrooms:
        filter_kwarg["bathrooms__lte"] = bathrooms
    if lat and lng:
        common = 0.005
        filter_kwarg["lat__gte"] = float(lat) - common
        filter_kwarg["lat__lte"] = float(lat) + common
        filter_kwarg["lng__gte"] = float(lng) - common
        filter_kwarg["lng__gte"] = float(lng) + common
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        rooms = Room.objects.filter(**filter_kwarg)
    except ValueError:
        rooms = Room.objects.prefetch_related()
    results = paginator.paginate_queryset(rooms, request=request)
    serializers = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializers.data)
