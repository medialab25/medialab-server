from datetime import datetime
from typing import Dict, List, Optional

import httpx
from pydantic import BaseModel

# Server configuration
SERVER_PORT = 4800


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None


class Notification(BaseModel):
    id: Optional[int] = None
    message: str
    timestamp: datetime = datetime.now()
    type: str
    data: Optional[Dict] = None


class MediaLabClient:
    def __init__(self, base_url: str = f"http://localhost:{SERVER_PORT}"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
        self.notifications: List[Notification] = []
        self._notification_id = 1

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def aclose(self):
        """Close the client's HTTP session."""
        await self.client.aclose()

    async def get_items(self) -> List[Item]:
        """Get all items from the server."""
        response = await self.client.get("/items")
        response.raise_for_status()
        return [Item(**item) for item in response.json()]

    async def get_item(self, item_id: int) -> Item:
        """Get a specific item by ID."""
        response = await self.client.get(f"/items/{item_id}")
        response.raise_for_status()
        return Item(**response.json())

    async def create_item(self, item: Item) -> Item:
        """Create a new item."""
        response = await self.client.post(
            "/items", json=item.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return Item(**response.json())

    async def update_item(self, item_id: int, item: Item) -> Item:
        """Update an existing item."""
        response = await self.client.put(
            f"/items/{item_id}", json=item.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return Item(**response.json())

    async def delete_item(self, item_id: int) -> dict:
        """Delete an item."""
        response = await self.client.delete(f"/items/{item_id}")
        response.raise_for_status()
        return response.json()

    def add_notification(self, notification: Notification) -> Notification:
        """Add a notification to the client's notification list."""
        notification.id = self._notification_id
        self._notification_id += 1
        self.notifications.append(notification)
        return notification

    def get_notifications(self) -> List[Notification]:
        """Get all notifications."""
        return self.notifications

    def clear_notifications(self) -> None:
        """Clear all notifications."""
        self.notifications.clear()
