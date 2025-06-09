import asyncio
import httpx
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from datetime import datetime

# Server configuration
SERVER_PORT = 4800
CLIENT_PORT = 4810

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
            "/items",
            json=item.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return Item(**response.json())

    async def update_item(self, item_id: int, item: Item) -> Item:
        """Update an existing item."""
        response = await self.client.put(
            f"/items/{item_id}",
            json=item.model_dump(exclude_none=True)
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

# Create FastAPI app for the client
app = FastAPI(
    title="MediaLab Client",
    description="Client application for MediaLab server with bidirectional communication",
    version="1.0.0"
)

# Create a single client instance to be used across the application
client = MediaLabClient()

@app.get("/")
async def root():
    """Root endpoint returning client information."""
    return {
        "message": "Welcome to MediaLab Client",
        "version": "1.0.0",
        "server_url": f"http://localhost:{SERVER_PORT}",
        "endpoints": {
            "items": "/items",
            "notifications": "/notifications",
            "server_communication": "/server-communication"
        }
    }

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items from the server."""
    return await client.get_items()

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item from the server."""
    return await client.get_item(item_id)

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """Create a new item on the server."""
    created_item = await client.create_item(item)
    # Add a notification about the creation
    client.add_notification(Notification(
        message=f"Created new item: {item.name}",
        type="item_created",
        data=created_item.model_dump()
    ))
    return created_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """Update an item on the server."""
    updated_item = await client.update_item(item_id, item)
    # Add a notification about the update
    client.add_notification(Notification(
        message=f"Updated item: {item.name}",
        type="item_updated",
        data=updated_item.model_dump()
    ))
    return updated_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item from the server."""
    result = await client.delete_item(item_id)
    # Add a notification about the deletion
    client.add_notification(Notification(
        message=f"Deleted item with ID: {item_id}",
        type="item_deleted"
    ))
    return result

@app.get("/notifications", response_model=List[Notification])
async def get_notifications():
    """Get all notifications."""
    return client.get_notifications()

@app.delete("/notifications")
async def clear_notifications():
    """Clear all notifications."""
    client.clear_notifications()
    return {"message": "All notifications cleared"}

@app.post("/server-communication/notify", response_model=Notification)
async def receive_server_notification(notification: Notification, background_tasks: BackgroundTasks):
    """Endpoint for the server to send notifications to the client."""
    # Store the notification
    stored_notification = client.add_notification(notification)
    
    # Example of background task: Process the notification
    background_tasks.add_task(process_notification, stored_notification)
    
    return stored_notification

async def process_notification(notification: Notification):
    """Process a notification in the background."""
    # Simulate some processing time
    await asyncio.sleep(1)
    print(f"Processed notification: {notification.message}")

@app.get("/server-communication/status")
async def get_communication_status():
    """Get the status of communication with the server."""
    try:
        # Try to get the server's root endpoint
        async with httpx.AsyncClient() as test_client:
            response = await test_client.get(f"http://localhost:{SERVER_PORT}/")
            server_status = "connected" if response.status_code == 200 else "error"
    except Exception as e:
        server_status = "disconnected"
    
    return {
        "client_status": "running",
        "server_status": server_status,
        "notifications_count": len(client.get_notifications()),
        "last_notification": client.get_notifications()[-1] if client.get_notifications() else None
    }

if __name__ == "__main__":
    # Run the client API server
    uvicorn.run(app, host="0.0.0.0", port=CLIENT_PORT) 