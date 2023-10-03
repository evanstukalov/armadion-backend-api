import time
from datetime import datetime, date
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from armadion import settings

# TODO test
class ContactFormSerializer(serializers.Serializer):
    current_date = serializers.DateField(default=date.today)
    current_time = serializers.DateTimeField(default=datetime.now, format=settings.DATETIME_FORMAT[1])

    user_name = serializers.CharField(max_length=60)
    phone_number = PhoneNumberField(region="RU")

    def save(self):
        """
        Saves the user data
        """

        # Get the username and phone number from the validated data
        user_name = self.validated_data['user_name']
        phone_number = self.validated_data['phone_number']

