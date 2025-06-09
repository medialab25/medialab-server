# MediaLab Services Publishing Guide

This guide covers how to build, publish, and deploy the MediaLab server and client services.

## Prerequisites

- Docker installed and configured
- Access to a container registry (Docker Hub, GitHub Container Registry, etc.)
- Docker Compose (for local development)

## Local Development

To run the services locally for development:

```bash
# Start both services with hot-reload
docker compose up

# Start in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Building Images

### Manual Build

Build the images individually:

```bash
# Build server image
docker build -t medialab-server:latest ./server

# Build client image
docker build -t medialab-client:latest ./client
```

### Using Docker Compose

```bash
# Build both images
docker compose build

# Build specific service
docker compose build server
docker compose build client
```

## Publishing Images

### 1. Tag Images

Tag the images for your container registry:

```bash
# For Docker Hub
docker tag medialab-server:latest yourusername/medialab-server:latest
docker tag medialab-client:latest yourusername/medialab-client:latest

# For GitHub Container Registry
docker tag medialab-server:latest ghcr.io/yourusername/medialab-server:latest
docker tag medialab-client:latest ghcr.io/yourusername/medialab-client:latest
```

### 2. Push to Registry

#### Docker Hub
```bash
# Login to Docker Hub
docker login

# Push images
docker push yourusername/medialab-server:latest
docker push yourusername/medialab-client:latest
```

#### GitHub Container Registry
```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push images
docker push ghcr.io/yourusername/medialab-server:latest
docker push ghcr.io/yourusername/medialab-client:latest
```

## Deployment

### Environment Variables

Both services support the following environment variables:

- `ENVIRONMENT`: Set to 'production' or 'development'
- `PYTHONPATH`: Set to '/app' in container
- `SERVER_URL`: Client service URL (for server service)
- `CLIENT_URL`: Server service URL (for client service)

### Production Deployment

1. Pull the images:
```bash
docker pull yourusername/medialab-server:latest
docker pull yourusername/medialab-client:latest
```

2. Run the services:
```bash
# Server
docker run -d \
  --name medialab-server \
  -p 4800:4800 \
  -e ENVIRONMENT=production \
  yourusername/medialab-server:latest

# Client
docker run -d \
  --name medialab-client \
  -p 4810:4810 \
  -e ENVIRONMENT=production \
  -e SERVER_URL=http://your-server-host:4800 \
  yourusername/medialab-client:latest
```

### Using Docker Compose in Production

Create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  server:
    image: yourusername/medialab-server:latest
    ports:
      - "4800:4800"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped

  client:
    image: yourusername/medialab-client:latest
    ports:
      - "4810:4810"
    environment:
      - ENVIRONMENT=production
      - SERVER_URL=http://server:4800
    depends_on:
      - server
    restart: unless-stopped
```

Run in production:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Security Considerations

1. Always use specific version tags in production, not just 'latest'
2. Regularly update base images and dependencies
3. Use secrets management for sensitive data
4. Implement proper network security between services
5. Consider using a reverse proxy in production

## Monitoring

The services expose health check endpoints:

- Server: `http://localhost:4800/health`
- Client: `http://localhost:4810/health`

Monitor these endpoints to ensure service health.

## Troubleshooting

Common issues and solutions:

1. **Connection Issues**
   - Verify network connectivity between services
   - Check environment variables for correct URLs
   - Ensure ports are not blocked by firewall

2. **Container Startup Issues**
   - Check container logs: `docker logs <container-name>`
   - Verify environment variables
   - Ensure proper permissions on mounted volumes

3. **Registry Issues**
   - Verify registry credentials
   - Check network connectivity to registry
   - Ensure proper image tagging 