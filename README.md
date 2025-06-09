# MediaLab Server

A FastAPI-based server application with a Python client for bidirectional communication.

## Project Structure

```
medialab-server/
├── .devcontainer/          # Development container configuration
├── common/                 # Common library package
│   ├── models.py          # Shared data models
│   ├── constants.py       # Shared constants
│   ├── utils.py           # Shared utilities
│   ├── __init__.py        # Package initialization
│   └── setup.py           # Package setup
├── server/                 # FastAPI server application
│   ├── app/               # Main application code
│   ├── tests/             # Server tests
│   └── requirements.txt    # Server dependencies
├── client/                # Python client application
│   ├── src/              # Client source code
│   ├── tests/            # Client tests
│   └── requirements.txt   # Client dependencies
└── README.md             # This file
```

## Common Library

The project includes a common library package that is shared between the server and client applications. This library provides:

- Shared data models (Item, Notification, StatusResponse)
- Common constants (ports, URLs, endpoints)
- Utility functions for:
  - Service status checking
  - Notification handling
  - Error response formatting
- Type definitions and enums
- Consistent validation rules

The common library is installed in editable mode in both the server and client applications, allowing for easy development and updates.

To use the common library in either application:

```python
from common import Item, Notification, NotificationType
from common import SERVER_URL, CLIENT_URL, Endpoints
from common import check_service_status, send_notification
```

## Development Setup

This project uses VS Code's Dev Containers for development. To get started:

1. Install [Docker](https://www.docker.com/products/docker-desktop)
2. Install [VS Code](https://code.visualstudio.com/)
3. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
4. Clone this repository
5. Open in VS Code and click "Reopen in Container" when prompted

## Running the Applications

### Server (Port 4800)

The FastAPI server runs on port 4800. To start it:

```bash
cd server
uvicorn app.main:app --reload --port 4800
```

The server provides:
- REST API for managing items
- Automatic client notifications for all item operations
- Client status monitoring
- API documentation at:
  - Swagger UI: http://localhost:4800/docs
  - ReDoc: http://localhost:4800/redoc

### Client (Port 4810)

The Python client runs on port 4810 and provides:
- REST API for client operations
- Bidirectional communication with the server
- Notification system for server events
- Status monitoring
- API documentation at:
  - Swagger UI: http://localhost:4810/docs
  - ReDoc: http://localhost:4810/redoc

To start the client:
```bash
cd client
python src/main.py
```

## Communication Features

### Server to Client
- Server automatically notifies client of all item operations (create, update, delete)
- Server can check client status via `/client-status` endpoint
- Notifications are processed asynchronously by the client

### Client to Server
- Client can perform all CRUD operations on server items
- Client maintains a notification history
- Client provides status information to the server
- All operations are performed asynchronously

## API Endpoints

### Server Endpoints
- `GET /` - Server information
- `GET /items` - List all items
- `GET /items/{id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item
- `GET /client-status` - Get client status

### Client Endpoints
- `GET /` - Client information
- `GET /items` - List all items from server
- `GET /items/{id}` - Get specific item from server
- `POST /items` - Create new item on server
- `PUT /items/{id}` - Update item on server
- `DELETE /items/{id}` - Delete item from server
- `GET /notifications` - List all notifications
- `DELETE /notifications` - Clear all notifications
- `POST /server-communication/notify` - Receive server notifications
- `GET /server-communication/status` - Get communication status

## Development

- Server API is built with FastAPI
- Client uses FastAPI for its own API
- Both applications use `httpx` for async HTTP requests
- Both applications use `pydantic` for data validation
- Testing is done with `pytest`
- Background tasks are used for async operations
- Notifications are processed asynchronously

## License

MIT
