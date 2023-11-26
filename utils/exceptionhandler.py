from rest_framework.response import Response
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    """
    The function `custom_exception_handler` handles custom exceptions by mapping them to specific
    handlers and returning a response with the appropriate status code and message.
    """
    try:
        exception_class = exc.__class__.__name__

        handlers = {
            'InvalidOperation': _handler_decimal_error
        }

        res = exception_handler(exc, context)

        if exception_class in handlers:
            # calling hanlder based on the custom  
            message, status_code = handlers[exception_class](exc, context, res)
        else:
            # if there is no hanlder is presnet
            message = str(exc)

        return Response(data={'errorMessage': message}, status=status_code)

    except Exception as e:
        logger.error(str(e))


def _handler_decimal_error(exc, context, res):
    """
    Handler for decimal errors
    """
    message = 'Invalid decimal value'
    status_code = 400
    return message, status_code