from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from contactform.serializers import ContactFormSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from contactform.services import add_new_row

# import the logging library
import logging

from contactform.tasks import task_execute

# Get an instance of a logger
logger = logging.getLogger(__name__)



@api_view(['POST'])
@swagger_auto_schema()
def contact_form(request: Request) -> Response:
    """
    Handle POST request to submit a contact form.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object.
    """

    try:
        # Create a serializer instance with the request data
        serializer = ContactFormSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the data from the serializer
            serializer.save()

        # If the serializer is not valid, return an error response with the serializer errors
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle any exceptions that occur during the execution of serializer.save()
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        task_execute(serializer.data)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution of add_new_row()
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return success response with the serialized data
    return Response(serializer.data, status=status.HTTP_201_CREATED)