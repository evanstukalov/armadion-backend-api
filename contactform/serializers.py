import time
from datetime import datetime, date
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from armadion import settings

class ContactFormSerializer(serializers.Serializer):
    current_date = serializers.DateTimeField(default=datetime.now(), format=settings.DATETIME_FORMAT[0], read_only=True)
    current_time = serializers.DateTimeField(default=datetime.now(), format=settings.DATETIME_FORMAT[1], read_only=True)

    user_name = serializers.CharField(max_length=60)
    phone_number = PhoneNumberField(region="RU")

    def save(self):
        """
        Saves the user data
        """

        # Get the username and phone number from the validated data
        user_name = self.validated_data['user_name']
        phone_number = self.validated_data['phone_number']

