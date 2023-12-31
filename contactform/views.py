from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from contactform.serializers import ContactFormSerializer
from contactform.tasks import task_execute


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

    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
