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

class SeriesSerializer(serializers.ModelSerializer):
    """
    Serializer for the series
    """
    door_type = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Door
        fields = ['name', 'description', 'photo', 'price_from', 'door_type']