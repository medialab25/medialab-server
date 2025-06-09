#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[MediaLab Dev]${NC} $1"
}

print_error() {
    echo -e "${RED}[MediaLab Dev Error]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[MediaLab Dev Warning]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if Docker Compose plugin is available
check_docker_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose plugin is not available. Please ensure Docker Compose plugin is installed on your host machine."
        exit 1
    fi
}

# Function to check if required ports are available
check_ports() {
    local ports=("4800" "4810")
    for port in "${ports[@]}"; do
        if lsof -i :$port > /dev/null 2>&1; then
            print_warning "Port $port is already in use. This might cause issues."
        fi
    done
}

# Function to start the development environment
start_dev() {
    print_message "Starting MediaLab development environment..."
    check_docker
    check_docker_compose
    check_ports
    
    # Build images if they don't exist
    if ! docker compose images | grep -q "medialab-server"; then
        print_message "Building images for the first time..."
        docker compose build
    fi
    
    # Start the services
    docker compose up -d
    
    # Wait for services to be ready
    print_message "Waiting for services to be ready..."
    sleep 5
    
    # Check if services are running
    if docker compose ps | grep -q "Up"; then
        print_message "Development environment is ready!"
        print_message "Server: http://localhost:4800/docs"
        print_message "Client: http://localhost:4810/docs"
        print_message "VS Code Dev Container: Use 'Reopen in Container' command in VS Code"
    else
        print_error "Failed to start services. Check logs with: ./scripts/dev.sh logs"
        exit 1
    fi
}

# Function to stop the development environment
stop_dev() {
    print_message "Stopping MediaLab development environment..."
    docker compose down
    print_message "Development environment stopped."
}

# Function to show logs
show_logs() {
    if [ "$1" == "server" ]; then
        docker compose logs -f server
    elif [ "$1" == "client" ]; then
        docker compose logs -f client
    else
        docker compose logs -f
    fi
}

# Function to rebuild services
rebuild() {
    print_message "Rebuilding services..."
    docker compose down
    docker compose build --no-cache
    start_dev
}

# Function to show status
show_status() {
    print_message "Service Status:"
    docker compose ps
}

# Function to show help
show_help() {
    echo "MediaLab Development Script"
    echo "Usage: ./scripts/dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start     Start the development environment (run this from host machine)"
    echo "  stop      Stop the development environment"
    echo "  restart   Restart the development environment"
    echo "  logs      Show logs (all, server, or client)"
    echo "  rebuild   Rebuild and restart the services"
    echo "  status    Show service status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/dev.sh start    # Run this from host machine"
    echo "  ./scripts/dev.sh logs server"
    echo "  ./scripts/dev.sh stop"
    echo ""
    echo "Note: This script should be run from your host machine, not from within the dev container."
}

# Main script logic
case "$1" in
    "start")
        start_dev
        ;;
    "stop")
        stop_dev
        ;;
    "restart")
        stop_dev
        start_dev
        ;;
    "logs")
        show_logs "$2"
        ;;
    "rebuild")
        rebuild
        ;;
    "status")
        show_status
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 