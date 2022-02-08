from rest_framework import viewsets
from .serializers import ReadRoomSerializer
from .models import Room


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.prefetch_related()
    serializer_class = ReadRoomSerializer
