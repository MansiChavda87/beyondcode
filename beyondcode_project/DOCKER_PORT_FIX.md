# Docker Port Conflict Resolution

## Problem
The error `ports are not available: exposing port TCP 0.0.0.0:8000 -> 127.0.0.1:0: listen tcp 0.0.0.0:8000: bind: An attempt was made to access a socket in a way forbidden by its access permissions` occurs when port 8000 is already in use by another service.

## Solution

### Option 1: Use Development Configuration (Recommended for local development)
The development configuration now uses port 8001 to avoid conflicts:

```bash
# Start development environment (uses port 8001)
docker-compose up

# Access your application at http://localhost:8001
```

### Option 2: Use Production Configuration
For production deployment, use the original port 8000:

```bash
# Start production environment (uses port 8000)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Access your application at http://localhost:8000
```

### Option 3: Stop Conflicting Services
If you need to use port 8000 for development, first stop any services using it:

```bash
# Check what's using port 8000
netstat -ano | findstr :8000
# or on Linux/Mac:
# lsof -i :8000

# Stop the conflicting service, then:
docker-compose up
```

### Option 4: Use Custom Port
You can also modify the port in the override file:

```yaml
# In docker-compose.override.yml, change:
ports:
  - "8002:8002"  # Use any available port
```

## Docker Commands

### Development (Port 8001)
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production (Port 8000)
```bash
# Start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Start in background
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Stop services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

## File Structure
- `docker-compose.yml` - Base configuration
- `docker-compose.override.yml` - Development overrides (port 8001)
- `docker-compose.prod.yml` - Production overrides (port 8000)

## Troubleshooting

### Port Still in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Docker Issues
```bash
# Clean up Docker
docker system prune -f

# Rebuild images
docker-compose build --no-cache

# Reset volumes (WARNING: This will delete data)
docker-compose down -v
docker-compose up --build