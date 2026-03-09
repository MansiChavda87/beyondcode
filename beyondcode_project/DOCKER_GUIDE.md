# Docker Setup Guide for BeyondCode Django Project

This guide provides comprehensive instructions for setting up and running the BeyondCode Django project using Docker.

## 🐳 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)
- At least 4GB RAM available for Docker

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd beyondcode_project
```

### 2. Start the Application

```bash
# Build and start all services
docker-compose up -d

# Or use the Makefile (recommended)
make start
```

### 3. Access the Application

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Default Admin**: admin / admin123

### 4. Seed Initial Content (Optional)

```bash
# Seed CMS content
make seed

# Or manually
docker-compose exec web python manage.py seed_cms_content
docker-compose exec web python manage.py seed_cms_admin
```

## 📁 Project Structure

```
beyondcode_project/
├── Dockerfile                    # Main Dockerfile for the web service
├── docker-compose.yml           # Development configuration
├── docker-compose.override.yml  # Development overrides
├── docker-compose.prod.yml      # Production configuration
├── docker-entrypoint.sh         # Container initialization script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── Makefile                     # Convenient commands
├── DOCKER_GUIDE.md             # This file
└── beyondcode_project/          # Django project
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Key Variables:**
- `DEBUG=True` - Enable debug mode (development only)
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `CLOUDINARY_URL` - Cloudinary media management (optional)

### Database Configuration

The project uses PostgreSQL by default in Docker. For development, you can use SQLite by modifying the `DATABASE_URL` in your `.env` file:

```bash
# For SQLite (development only)
DATABASE_URL=sqlite:///db.sqlite3
```

To use SQLite, you'll also need to modify `docker-compose.yml` to remove the PostgreSQL service and update the web service configuration.

## 🐳 Docker Commands

### Using Makefile (Recommended)

```bash
# Build images
make build

# Start services
make start

# View logs
make logs

# Run Django commands
make migrate
make createsuperuser
make shell

# Seed content
make seed

# Clean up
make clean

# Get help
make help
```

### Using Docker Compose Directly

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (resets database)
docker-compose down -v

# Run commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 🚀 Development Workflow

### 1. Start Development Environment

```bash
# Start with development overrides
make dev-up
# or
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 2. Make Changes

The development environment mounts your local code into the container, so changes are reflected immediately.

### 3. Run Migrations (if needed)

```bash
make migrate
```

### 4. View Logs

```bash
make logs
# or filter logs
docker-compose logs -f web
```

### 5. Access Django Shell

```bash
make shell
# or
docker-compose exec web python manage.py shell
```

### 6. Access Database

```bash
# PostgreSQL shell
docker-compose exec db psql -U postgres -d beyondcode_db

# Or use Django ORM
make shell
# Then in Django shell:
# from django.db import connection
# cursor = connection.cursor()
```

## 🏗️ Production Deployment

### 1. Prepare Production Environment

```bash
# Create production environment file
cp .env.example .env.prod

# Edit .env.prod with production values
# Required: SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS, POSTGRES_PASSWORD
```

### 2. Deploy

```bash
# Build and start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 3. Set Up Reverse Proxy

See the production deployment section in README.md for Nginx configuration and SSL setup.

## 🔍 Troubleshooting

### Common Issues

**1. Port 8000 already in use**
```bash
# Find and stop the process using port 8000
sudo lsof -i :8000
# Or change the port in docker-compose.yml
```

**2. Database connection issues**
```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

**3. Permission issues with media files**
```bash
# Ensure media directory exists and has correct permissions
mkdir -p media
chmod 755 media
```

**4. Container won't start**
```bash
# Check container logs
docker-compose logs web

# Check if dependencies are installed
docker-compose exec web pip list

# Rebuild container
docker-compose build --no-cache web
docker-compose up -d web
```

### Debug Commands

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats

# Check Docker images
docker images

# Check Docker volumes
docker volume ls

# Clean up unused resources
docker system prune
```

## 🧪 Testing

### Run Tests

```bash
# Run the comprehensive test suite
make test
# or
docker-compose exec web python test_cms_functionality.py

# Run Django tests
docker-compose exec web python manage.py test marketing
```

### Test Database

The test suite uses a separate test database. To run tests with a clean database:

```bash
# Stop services
make stop

# Remove volumes (this will delete all data)
make clean

# Start fresh
make start

# Run tests
make test
```

## 📊 Performance Optimization

### Development

- Code changes are automatically reflected (hot reload)
- Debug mode is enabled
- Database is persistent between restarts

### Production

- Gunicorn with 3 workers
- Health checks enabled
- No volume mounts (faster performance)
- Security headers enabled

### Caching

Redis is included for caching. To enable caching in Django:

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}
```

## 🔐 Security

### Development
- Debug mode enabled
- Default secret key
- Local database access

### Production
- Debug mode disabled
- Secure secret key required
- HTTPS enforced
- Secure cookies enabled
- Database password required

## 🔄 Updates and Maintenance

### Update Dependencies

1. Update `requirements.txt`
2. Rebuild images:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Backup Database

```bash
# Backup
docker-compose exec db pg_dump -U postgres beyondcode_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres -d beyondcode_db < backup.sql
```

### Update Docker Images

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest images
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

## 📞 Support

For Docker-related issues:

1. Check the troubleshooting section above
2. View container logs: `docker-compose logs`
3. Check Docker resources: `docker system df`
4. Clean up and restart: `make clean && make start`

For Django-specific issues, refer to the main README.md or Django documentation.

---

**Note**: This Docker setup is designed for both development and production use. Always use appropriate security measures in production environments.