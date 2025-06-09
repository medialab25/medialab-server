from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    """Types of notifications that can be sent between server and client."""
    ITEM_CREATED = "item_created"
    ITEM_UPDATED = "item_updated"
    ITEM_DELETED = "item_deleted"
    SERVER_ITEM_CREATED = "server_item_created"
    SERVER_ITEM_UPDATED = "server_item_updated"
    SERVER_ITEM_DELETED = "server_item_deleted"
    SYSTEM_NOTIFICATION = "system_notification"

class Item(BaseModel):
    """Common item model used by both server and client."""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Item",
                "description": "This is an example item"
            }
        }

class Notification(BaseModel):
    """Common notification model for server-client communication."""
    id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=500)
    timestamp: datetime = Field(default_factory=datetime.now)
    type: NotificationType
    data: Optional[Dict] = None
    source: str = Field(..., description="Source of the notification (server/client)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Item created successfully",
                "type": "item_created",
                "source": "server",
                "data": {"item_id": 1, "name": "Example Item"}
            }
        }

class StatusResponse(BaseModel):
    """Common status response model."""
    status: str = Field(..., description="Current status (running/error/disconnected)")
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "running",
                "version": "1.0.0",
                "details": {"items_count": 5, "notifications_count": 10}
            }
        } 