from .models import Room
from rest_framework import serializers
from users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ["modified"]
        read_only_fields = ["user", "id"]

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
