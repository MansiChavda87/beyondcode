# How to Run This Project

This Django-based marketing website and CMS can be run in multiple ways. Below are detailed instructions for each approach.

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Steps

1. **Navigate to the project directory**
   ```bash
   cd beyondcode_project
   ```

2. **Start the application using Docker Compose**
   ```bash
   docker-compose up -d
   ```
   This will:
   - Build the Django application container
   - Start PostgreSQL database
   - Start Redis for caching
   - Expose the application on port 8000

3. **Access the application**
   - **Website**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin
   - **Default admin credentials**: admin / admin123

4. **Seed initial content (optional but recommended)**
   ```bash
   # Seed CMS content
   docker-compose exec web python manage.py seed_cms_content
   
   # Create admin user
   docker-compose exec web python manage.py seed_cms_admin
   ```

5. **View logs to monitor the application**
   ```bash
   docker-compose logs -f
   ```

## 🛠️ Alternative: Using Makefile Commands

The project includes a Makefile with convenient commands:

```bash
# Build Docker images
make build

# Start all services
make start

# View logs
make logs

# Run database migrations
make migrate

# Create superuser
make createsuperuser

# Seed initial content
make seed

# Stop all services
make stop

# Clean up everything
make clean
```

## 💻 Local Development (Without Docker)

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or SQLite

### Steps

1. **Navigate to the project directory**
   ```bash
   cd beyondcode_project
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings (optional for basic functionality)
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - **Website**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin

## 📋 Available Commands and Endpoints

### Django Management Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed CMS content
python manage.py seed_cms_content

# Seed admin user
python manage.py seed_cms_admin

# Open Django shell
python manage.py shell

# Check for any issues
python manage.py check
```

### Application Endpoints
- **Home Page**: `/`
- **Blog**: `/blog/`
- **Admin Panel**: `/admin/`
- **CMS Dashboard**: `/marketing/cms/dashboard/`
- **Block Builder**: `/marketing/cms/blocks/builder/`
- **API Endpoints**: `/marketing/api/`
- **Sitemap**: `/sitemap.xml`
- **Robots.txt**: `/robots.txt`

### Docker Commands
```bash
# View running containers
docker-compose ps

# View logs from specific service
docker-compose logs -f web
docker-compose logs -f db

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell

# Stop and remove containers
docker-compose down

# Stop and remove volumes (resets database)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file in the project root with these optional settings:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (SQLite is default, PostgreSQL recommended for production)
DATABASE_URL=sqlite:///db.sqlite3
# Or for PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Cloudinary (for media management - optional)
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Database Options

**SQLite (Default - No setup required)**
- Perfect for development and testing
- Data stored in `db.sqlite3` file

**PostgreSQL (Recommended for production)**
- More robust and scalable
- Requires PostgreSQL server setup
- Configure with `DATABASE_URL` environment variable

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Using the custom test file
python test_cms_functionality.py

# Or using Django's test runner
python manage.py test marketing
```

## 🐛 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Find what's using port 8000
   lsof -i :8000
   
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database connection issues**
   ```bash
   # Check if database container is running
   docker-compose ps
   
   # View database logs
   docker-compose logs db
   ```

3. **Permission errors**
   ```bash
   # Ensure proper permissions on project files
   chmod -R 755 .
   ```

4. **Missing dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

### Docker-Specific Issues

1. **Build failures**
   ```bash
   # Clean and rebuild
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

2. **Volume permission issues**
   ```bash
   # Reset volumes
   docker-compose down -v
   docker-compose up -d
   ```

## 🚀 Production Deployment

For production deployment, use the production Docker Compose file:

```bash
# Build and start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run production migrations
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 📚 Project Structure Overview

```
beyondcode_project/
├── beyondcode_project/     # Django project settings
├── marketing/             # Main Django app with CMS functionality
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Docker build instructions
└── README.md          # Project documentation
```

## 🎯 Next Steps

1. **Explore the Admin Panel**: http://localhost:8000/admin
2. **Use the CMS Dashboard**: http://localhost:8000/marketing/cms/dashboard/
3. **Try the Block Builder**: http://localhost:8000/marketing/cms/blocks/builder/
4. **Check the Blog**: http://localhost:8000/blog/
5. **Review the API**: http://localhost:8000/marketing/api/

The application is now ready for development, content management, or production use!