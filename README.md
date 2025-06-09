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
│   ├── src/              # Server source code
│   ├── tests/            # Server tests
│   └── requirements.txt   # Server dependencies
├── client/                # Python client application
│   ├── src/              # Client source code
│   ├── tests/            # Client tests
│   └── requirements.txt   # Client dependencies
├── scripts/              # Development and deployment scripts
│   └── dev.sh           # Development environment script
├── docker-compose.yml    # Service orchestration
└── README.md            # This file
```

## Development Setup

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your host machine
- [VS Code](https://code.visualstudio.com/) with [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension

### Starting Development

1. Start the development environment from your host machine:
   ```bash
   ./scripts/dev.sh start
   ```
   This will:
   - Build and start the server and client containers
   - Set up hot-reload for both services
   - Make services available at:
     - Server: http://localhost:4800/docs
     - Client: http://localhost:4810/docs

2. Open VS Code and use "Reopen in Container" command
   - This will open a development container with:
     - Python development tools
     - Code formatting (black)
     - Linting (pylint)
     - Testing (pytest)
     - Type checking (mypy)

### Development Workflow

1. **Host Machine** (for Docker operations):
   ```bash
   # Start services
   ./scripts/dev.sh start

   # View logs
   ./scripts/dev.sh logs

   # Stop services
   ./scripts/dev.sh stop

   # Rebuild services
   ./scripts/dev.sh rebuild
   ```

2. **VS Code Dev Container** (for development):
   - Edit code with full IDE support
   - Automatic formatting on save
   - Integrated testing
   - Type checking
   - Hot-reload enabled for both services

## Services

### Server (Port 4800)

FastAPI server providing:
- REST API for managing items
- Automatic client notifications
- API documentation at:
  - Swagger UI: http://localhost:4800/docs
  - ReDoc: http://localhost:4800/redoc

### Client (Port 4810)

FastAPI client providing:
- REST API for client operations
- Bidirectional communication with server
- Notification system
- API documentation at:
  - Swagger UI: http://localhost:4810/docs
  - ReDoc: http://localhost:4810/redoc

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

## Development Tools

The development container includes:
- Python 3.11
- Black (code formatting)
- Pylint (code linting)
- Pytest (testing)
- MyPy (type checking)
- Git (version control)

## License

MIT
