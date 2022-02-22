from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .serializers import RoomSerializer


# # Create your views here.
# @api_view(["GET"])
# def list_rooms(request):
#     room = Room.objects.prefetch_related()
#     serialized_room = RoomSerializer(room, many=True)
#     return Response(data=serialized_room.data)
#
# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.prefetch_related()
#     serializer_class = RoomSerializer
#
# @api_view(["GET", "POST"])
# def room_view(request):
#     if request.method == "GET":
#
#
#     elif request.method == "POST":


class RoomsView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        rooms = Room.objects.prefetch_related()
        result = paginator.paginate_queryset(rooms, request=request)
        serializer = RoomSerializer(result, many=True).data
        return paginator.get_paginated_response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=room_serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room:
            serializer = RoomSerializer(room).data
            return Response(data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        room = self.get_room(pk)
        if room:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response(data=serializer.data)+
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
