from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


# Create your views here.
@api_view(["GET"])
def list_rooms(request):
    room = Room.objects.prefetch_related()
    serialized_room = RoomSerializer(room, many=True)
    return Response(data=serialized_room.data)
