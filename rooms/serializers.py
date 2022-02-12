from .models import Room
from rest_framework import serializers
from users.serializers import RelatedUserSerializer


class ReadRoomSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = []


class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ["id", "user", "modified"]

    def validate_beds(self, beds):
        if beds < 5:
            raise serializers.ValidationError("your room is too small")
        else:
            return beds

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")

            if check_in == check_out:
                raise serializers.ValidationError("can't happen pal")
        return data
