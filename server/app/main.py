from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import httpx
from datetime import datetime

# Client configuration
CLIENT_PORT = 4810

app = FastAPI(
    title="MediaLab API",
    description="API for MediaLab server application with client communication",
    version="1.0.0"
)

# Data models
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

# In-memory storage (replace with database in production)
items: List[Item] = []
current_id = 1

async def notify_client(notification: Notification):
    """Send a notification to the client."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{CLIENT_PORT}/server-communication/notify",
                json=notification.model_dump()
            )
            response.raise_for_status()
    except Exception as e:
        print(f"Failed to notify client: {e}")

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to MediaLab API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "client_url": f"http://localhost:{CLIENT_PORT}"
    }

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items."""
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID."""
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item, background_tasks: BackgroundTasks):
    """Create a new item."""
    global current_id
    item.id = current_id
    current_id += 1
    items.append(item)
    
    # Notify the client about the new item
    notification = Notification(
        message=f"Server created new item: {item.name}",
        type="server_item_created",
        data=item.model_dump()
    )
    background_tasks.add_task(notify_client, notification)
    
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item, background_tasks: BackgroundTasks):
    """Update an existing item."""
    for i, item in enumerate(items):
        if item.id == item_id:
            updated_item.id = item_id
            items[i] = updated_item
            
            # Notify the client about the update
            notification = Notification(
                message=f"Server updated item: {updated_item.name}",
                type="server_item_updated",
                data=updated_item.model_dump()
            )
            background_tasks.add_task(notify_client, notification)
            
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, background_tasks: BackgroundTasks):
    """Delete an item."""
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)
            
            # Notify the client about the deletion
            notification = Notification(
                message=f"Server deleted item with ID: {item_id}",
                type="server_item_deleted",
                data={"item_id": item_id}
            )
            background_tasks.add_task(notify_client, notification)
            
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/client-status")
async def get_client_status():
    """Get the status of the client."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:{CLIENT_PORT}/server-communication/status")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get client status: {str(e)}"
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4800, reload=True) 