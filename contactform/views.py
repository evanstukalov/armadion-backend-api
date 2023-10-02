from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from contactform.serializers import ContactFormSerializer
from rest_framework import status

@api_view(['POST'])
def contact_form(request: Request) -> Response:
    """
    Handle POST request to submit a contact form.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object.

    """
    # Create a serializer instance with the request data
    serializer = ContactFormSerializer(data=request.data)

    # If the serializer is valid, save the data and return a success response
    if serializer.is_valid():
        serializer.save()
        # TODO: функция добавления в google sheets

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return an error response with the serializer errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)