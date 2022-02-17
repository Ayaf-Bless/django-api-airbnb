from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import ReadUserSerializer, WriteUserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rooms.serializers import RoomSerializer
from .models import User


# Create your views here.


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(klass=User, pk=pk)
        return Response(ReadUserSerializer(user).data, status=status.HTTP_200_OK)


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

    def post(self, request):
        pass
