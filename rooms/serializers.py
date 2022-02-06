from .models import Room
from rest_framework import serializers
from users.serializers import TinyUserSerializer


class RoomSerializerList(serializers.ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ["id", "name", "price", "bedrooms", "user"]


class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Room
        exclude = []
