from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from contactform.serializers import ContactFormSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


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
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        task_execute(serializer.data)
        logger.warning(serializer.data)

    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.data, status=status.HTTP_201_CREATED)