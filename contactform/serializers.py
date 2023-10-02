from datetime import datetime
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField



class ContactFormSerializer(serializers.Serializer):
    current_time = serializers.DateTimeField(default=datetime.now(), format='%Y-%m-%d %H:%M')
    user_name = serializers.CharField(max_length=60)
    phone_number = PhoneNumberField(region="RU")

    def save(self):
        """
        Saves the user data with current timestamp.
        """
        # Get the current time
        current_time = datetime.now()
        print(f"Current time: {current_time}")

        # Get the username and phone number from the validated data
        user_name = self.validated_data['user_name']
        print(f"User name: {user_name}")
        phone_number = self.validated_data['phone_number']
        print(f"Phone number: {phone_number}")

