from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


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

@api_view(["GET", "POST"])
def room_view(request):
    if request.method == "GET":
        rooms = Room.objects.prefetch_related()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.prefetch_related()
    serializer_class = ReadRoomSerializer
