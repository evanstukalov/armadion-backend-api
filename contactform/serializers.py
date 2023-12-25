from datetime import datetime

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

class ContactFormSerializer(serializers.Serializer):
    current_date = serializers.SerializerMethodField()
    current_time = serializers.SerializerMethodField()
    user_name = serializers.CharField(max_length=60)
    phone_number = PhoneNumberField(region="RU")

    def get_current_date(self, obj):
        return datetime.now().isoformat()

    def get_current_time(self, obj):
        return datetime.now().isoformat()

    def save(self):
        """
        Saves the user data
        """

        # Get the username and phone number from the validated data
        user_name = self.validated_data['user_name']
        phone_number = self.validated_data['phone_number']
