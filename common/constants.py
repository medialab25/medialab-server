"""Common constants used by both server and client."""

# Server configuration
SERVER_PORT = 4800
SERVER_HOST = "0.0.0.0"
SERVER_URL = f"http://localhost:{SERVER_PORT}"

# Client configuration
CLIENT_PORT = 4810
CLIENT_HOST = "0.0.0.0"
CLIENT_URL = f"http://localhost:{CLIENT_PORT}"

# API endpoints
class Endpoints:
    """Common API endpoint paths."""
    # Server endpoints
    SERVER_ROOT = "/"
    SERVER_ITEMS = "/items"
    SERVER_ITEM = "/items/{item_id}"
    SERVER_CLIENT_STATUS = "/client-status"
    
    # Client endpoints
    CLIENT_ROOT = "/"
    CLIENT_ITEMS = "/items"
    CLIENT_ITEM = "/items/{item_id}"
    CLIENT_NOTIFICATIONS = "/notifications"
    CLIENT_SERVER_COMMUNICATION = "/server-communication"
    CLIENT_NOTIFY = "/server-communication/notify"
    CLIENT_STATUS = "/server-communication/status"

# API versions
API_VERSION = "1.0.0"

# Error messages
class ErrorMessages:
    """Common error messages."""
    ITEM_NOT_FOUND = "Item not found"
    CLIENT_NOT_AVAILABLE = "Client is not available"
    SERVER_NOT_AVAILABLE = "Server is not available"
    INVALID_REQUEST = "Invalid request"
    INTERNAL_ERROR = "Internal server error" 