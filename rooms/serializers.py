from .models import Room
from rest_framework import serializers
from users.serializers import TinyUserSerializer


class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ["name", "price", "bedrooms", "user"]
