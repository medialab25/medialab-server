"""Common utilities used by both server and client."""
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
from .constants import SERVER_URL, CLIENT_URL, ErrorMessages
from .models import StatusResponse, Notification, NotificationType

async def check_service_status(url: str) -> StatusResponse:
    """Check the status of a service (server or client)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/")
            response.raise_for_status()
            data = response.json()
            return StatusResponse(
                status="running",
                version=data.get("version", "unknown"),
                details={"response": data}
            )
    except Exception as e:
        return StatusResponse(
            status="error",
            version="unknown",
            details={"error": str(e)}
        )

async def send_notification(
    target_url: str,
    notification: Notification,
    timeout: float = 5.0
) -> Optional[Notification]:
    """Send a notification to a service."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{target_url}/server-communication/notify",
                json=notification.model_dump(),
                timeout=timeout
            )
            response.raise_for_status()
            return Notification(**response.json())
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return None

def create_notification(
    message: str,
    notification_type: NotificationType,
    source: str,
    data: Optional[Dict[str, Any]] = None
) -> Notification:
    """Create a notification with current timestamp."""
    return Notification(
        message=message,
        type=notification_type,
        source=source,
        data=data,
        timestamp=datetime.now()
    )

def format_error_response(
    message: str,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Format a consistent error response."""
    return {
        "error": {
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
    } 