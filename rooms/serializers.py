from .models import Room
from rest_framework import serializers
from users.serializers import UserSerializer



class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Room
        exclude = []
