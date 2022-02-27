from django.shortcuts import render
import jwt
from rest_framework.viewsets import ModelViewSet
from rooms.models import Room
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.permission import IsSelf
from users.serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rooms.serializers import RoomSerializer
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings


# Create your views here.
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf, IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, url_name="login", methods=["post"])
    def login_view(self, request):
        password = request.data.get("password")
        username = request.data.get("username")
        if not password and not username:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        encoded_jwt = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")
        return Response(data={"token": encoded_jwt, id: user.pk})

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializers = RoomSerializer(user.favs.all(), many=True)
        return Response(serializers.data)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        user = request.user
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        room = get_object_or_404(klass=Room, pk=pk)
        if room in user.favs.all():
            user.favs.remove(room)
        else:
            user.favs.add(room)
        return Response(status=status.HTTP_200_OK)

