from rest_framework import serializers
from doors.models import Door


class MainPageCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for the main page catalog
    """

    class Meta:
        model = Door
        fields = ['photo', 'title', 'price', 'article']

