from rest_framework import serializers
from doors.models import Door


class DoorCarouselSerializer(serializers.ModelSerializer):
    """
    Serializer for the door carousel
    """
    door_type = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Door
        fields = ['name', 'photo', 'in_stock', 'door_type', 'price']