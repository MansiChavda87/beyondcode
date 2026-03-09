# Makefile for BeyondCode Django Project

.PHONY: help build start stop restart logs shell dbshell migrate createsuperuser seed clean test

# Default target
help:
	@echo "Available commands:"
	@echo "  build        - Build Docker images"
	@echo "  start        - Start all services"
	@echo "  stop         - Stop all services"
	@echo "  restart      - Restart all services"
	@echo "  logs         - View logs from all services"
	@echo "  shell        - Open shell in web container"
	@echo "  dbshell      - Open database shell"
	@echo "  migrate      - Run database migrations"
	@echo "  createsuperuser - Create Django superuser"
	@echo "  seed         - Seed initial content"
	@echo "  clean        - Clean up containers and volumes"
	@echo "  test         - Run tests"

# Build Docker images
build:
	docker-compose build

# Start all services
start:
	docker-compose up -d

# Stop all services
stop:
	docker-compose down

# Restart all services
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# Open shell in web container
shell:
	docker-compose exec web python manage.py shell

# Open database shell
dbshell:
	docker-compose exec db psql -U postgres -d beyondcode_db

# Run database migrations
migrate:
	docker-compose exec web python manage.py migrate

# Create Django superuser
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Seed initial content
seed:
	docker-compose exec web python manage.py seed_cms_content
	docker-compose exec web python manage.py seed_cms_admin

# Clean up containers and volumes
clean:
	docker-compose down -v
	docker system prune -f

# Run tests
test:
	docker-compose exec web python test_cms_functionality.py

# Development commands
dev-up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

dev-down:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml down

# Production commands (when you have docker-compose.prod.yml)
prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down