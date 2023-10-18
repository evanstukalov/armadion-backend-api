from django.urls import reverse
import pytest


class TestContactFormEndpoints:
    url = reverse('contactform:contact-form')

    @pytest.mark.parametrize('user_name, phone_number, status_code',
                             [
                                 ('user_test', '+79999999999', 201),
                                 ('user_test', '89999999999', 201),
                                 ('user_test', '+799999999', 400),
                                 ('user_test', '899999999', 400),
                                 ('', '+79999999999', 400),
                                 ('user_test', '', 400),
                             ])
    def test_post(self, user_name, phone_number, status_code, api_client):
        # Arrange
        request_data = {
            'current_date': '2022-01-01',
            'current_time': '12:00:00',
            "user_name": user_name,
            "phone_number": phone_number
        }

        # Act

        response = api_client.post(
            self.url,
            data=request_data)

        # Assert
        assert response.status_code == status_code
