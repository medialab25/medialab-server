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
    check_ports
    
    # Start the server
    print_message "Starting server..."
    cd server && npm run dev &
    SERVER_PID=$!
    
    # Start the client
    print_message "Starting client..."
    cd ../client && npm run dev &
    CLIENT_PID=$!
    
    # Save PIDs to a file for later use
    echo "$SERVER_PID" > .dev.pid
    echo "$CLIENT_PID" >> .dev.pid
    
    print_message "Development environment is ready!"
    print_message "Server: http://localhost:4800/docs"
    print_message "Client: http://localhost:4810/docs"
}

# Function to stop the development environment
stop_dev() {
    print_message "Stopping MediaLab development environment..."
    if [ -f .dev.pid ]; then
        while read pid; do
            if ps -p $pid > /dev/null; then
                kill $pid
            fi
        done < .dev.pid
        rm .dev.pid
    fi
    print_message "Development environment stopped."
}

# Function to show logs
show_logs() {
    if [ "$1" == "server" ]; then
        tail -f server/logs/app.log
    elif [ "$1" == "client" ]; then
        tail -f client/logs/app.log
    else
        tail -f server/logs/app.log client/logs/app.log
    fi
}

# Function to show status
show_status() {
    print_message "Service Status:"
    if [ -f .dev.pid ]; then
        while read pid; do
            if ps -p $pid > /dev/null; then
                echo "Process $pid is running"
            else
                echo "Process $pid is not running"
            fi
        done < .dev.pid
    else
        print_warning "No running processes found"
    fi
}

# Function to show help
show_help() {
    echo "MediaLab Development Script"
    echo "Usage: ./scripts/dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start     Start the development environment"
    echo "  stop      Stop the development environment"
    echo "  restart   Restart the development environment"
    echo "  logs      Show logs (all, server, or client)"
    echo "  status    Show service status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/dev.sh start"
    echo "  ./scripts/dev.sh logs server"
    echo "  ./scripts/dev.sh stop"
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