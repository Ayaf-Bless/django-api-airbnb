from django.shortcuts import render
import jwt
from rest_framework.viewsets import ModelViewSet
from rooms.models import Room
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
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
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(klass=User, pk=pk)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_fav(request):
    room = request.data.get("room")
    print(room)


class FavView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializers = RoomSerializer(user.favs.all(), many=True)
        return Response(serializers.data)

    def patch(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        room = get_object_or_404(klass=Room, pk=pk)
        if room in user.favs.all():
            user.favs.remove(room)
        else:
            user.favs.add(room)
        return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def login_view(request):
    password = request.data.get("password")
    username = request.data.get("username")
    if not password and not username:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    encoded_jwt = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")
    return Response(data={"token": encoded_jwt})
