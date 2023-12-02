from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def error404(request, exception):
    message = 'Not found'
    status_code = 404

    return Response(data={'errorMessage': message}, status=status_code)

@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def error500(request, exception):
    message = 'An error occured, it`s on us'
    status_code = 500

    return Response(data={'errorMessage': message}, status=status_code)