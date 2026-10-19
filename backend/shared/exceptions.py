from rest_framework.response import Response
from rest_framework.views import exception_handler


class ServiceError(Exception):
    """A business rule was broken. The message is safe to show to the user."""

    def __init__(self, message: str, code: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status


def api_exception_handler(exc, context):
    if isinstance(exc, ServiceError):
        return Response({"detail": exc.message, "code": exc.code}, status=exc.status)
    return exception_handler(exc, context)
