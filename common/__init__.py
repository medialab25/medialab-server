"""Common Library for MediaLab Server and Client.

This package contains shared models, utilities, and constants used by both
the server and client applications.
"""

from .models import Item, Notification, NotificationType, StatusResponse
from .constants import (
    SERVER_PORT,
    CLIENT_PORT,
    SERVER_URL,
    CLIENT_URL,
    Endpoints,
    API_VERSION,
    ErrorMessages
)
from .utils import (
    check_service_status,
    send_notification,
    create_notification,
    format_error_response
)

__version__ = "0.1.0"
__all__ = [
    "Item",
    "Notification",
    "NotificationType",
    "StatusResponse",
    "SERVER_PORT",
    "CLIENT_PORT",
    "SERVER_URL",
    "CLIENT_URL",
    "Endpoints",
    "API_VERSION",
    "ErrorMessages",
    "check_service_status",
    "send_notification",
    "create_notification",
    "format_error_response"
] 