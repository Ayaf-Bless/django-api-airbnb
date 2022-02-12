from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import ReadUserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User


# Create your views here.


class Me(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(ReadUserSerializer(request.user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        pass


class UserView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(klass=User, pk=pk)
        return Response(ReadUserSerializer(user).data, status=status.HTTP_200_OK)
