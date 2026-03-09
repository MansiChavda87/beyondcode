# BeyondCode AI - Marketing Website & CMS

A comprehensive Django-based marketing website and content management system built for BeyondCode AI, featuring a modern design, powerful CMS capabilities, and extensive customization options.

## 🚀 Features

### Core Website Features
- **Pixel-perfect homepage** based on provided design
- **Blog system** with categories, tags, and pagination
- **Page management** with rich content blocks
- **SEO optimization** with sitemap and robots.txt
- **Responsive design** that works on all devices
- **Accessibility** with proper ARIA labels and keyboard navigation

### CMS Features
- **Drag-and-drop block builder** for content creation
- **12+ content blocks** including rich text, callouts, features, CTAs, pricing tables, FAQs, and more
- **Media management** with Cloudinary integration
- **User permissions** system for content management
- **API endpoints** for programmatic access
- **Real-time preview** of content changes
- **Template system** for consistent styling

### Technical Features
- **Modern Django architecture** with clean separation of concerns
- **RESTful API** endpoints for all major functionality
- **Custom template tags** for enhanced functionality
- **Management commands** for seeding content
- **Comprehensive testing** suite
- **Design system** with CSS custom properties
- **Performance optimized** with caching and lazy loading

## 📁 Project Structure

```
beyondcode_project/
├── beyondcode_project/          # Django project configuration
│   ├── settings.py             # Main settings with environment variables
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI application
├── marketing/                  # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # View functions and classes
│   ├── urls.py                # App URL patterns
│   ├── forms.py               # Django forms
│   ├── permissions.py         # Permission system
│   ├── blocks.py              # Content block definitions
│   ├── renderers.py           # Block rendering logic
│   ├── templatetags/          # Custom template tags
│   ├── management/commands/   # Management commands
│   ├── templates/             # HTML templates
│   │   ├── marketing/
│   │   │   ├── base.html      # Base template
│   │   │   ├── pages/         # Page templates
│   │   │   ├── blog/          # Blog templates
│   │   │   ├── cms/           # CMS admin templates
│   │   │   ├── blocks/        # Block rendering templates
│   │   │   └── seo/           # SEO templates
│   └── static/                # Static files
│       └── marketing/
│           ├── css/           # Stylesheets
│           │   ├── main.css   # Main design system
│           │   └── block-builder.css  # Block builder styles
│           └── js/            # JavaScript files
│               ├── main.js    # Main JavaScript
│               └── block-builder.js  # Block builder functionality
├── test_cms_functionality.py  # Comprehensive test suite
└── README.md                  # This file
```

## 🛠️ Installation

### Option 1: Docker (Recommended)

#### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

#### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd beyondcode_project
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Website: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - Default admin credentials: admin / admin123

4. **Seed initial content (optional)**
   ```bash
   docker-compose exec web python manage.py seed_cms_content
   docker-compose exec web python manage.py seed_cms_admin
   ```

5. **View logs**
   ```bash
   docker-compose logs -f web
   ```

6. **Stop the application**
   ```bash
   docker-compose down
   ```

#### Docker Commands

Using docker-compose directly:
```bash
# Build and start all services
docker-compose up -d

# Start only the web service
docker-compose up -d web

# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Access database
docker-compose exec db psql -U postgres -d beyondcode_db

# Stop all services
docker-compose down

# Stop and remove volumes (resets database)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

Using Makefile (recommended):
```bash
# Build images
make build

# Start all services
make start

# View logs
make logs

# Run Django commands
make migrate
make createsuperuser
make shell

# Seed initial content
make seed

# Clean up everything
make clean

# See all available commands
make help
```

### Option 2: Local Development

#### Prerequisites
- Python 3.8+
- Django 4.2+
- PostgreSQL (recommended) or SQLite
- Cloudinary account (for media management)

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd beyondcode_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Seed initial content**
   ```bash
   python manage.py seed_cms_content
   python manage.py seed_cms_admin
   ```

## 🎨 Design System

The project uses a comprehensive design system with CSS custom properties:

### Color Palette
- Primary: `#2563eb` (Blue)
- Secondary: `#16a34a` (Green)
- Danger: `#dc2626` (Red)
- Warning: `#f59e0b` (Orange)
- Info: `#3b82f6` (Light Blue)

### Typography
- Font Family: System fonts with fallbacks
- Font Sizes: 12px to 60px scale
- Line Height: 1.5 for optimal readability

### Spacing
- Scale: 4px to 96px (xs to 4xl)
- Consistent spacing throughout the design

### Components
- Buttons with multiple variants
- Cards with hover effects
- Forms with validation states
- Navigation with responsive behavior

## 🧩 Content Blocks

The CMS supports 12+ content blocks:

1. **Rich Text** - Editor.js-powered rich text content
2. **Callout** - Highlight important information
3. **Feature Grid** - Display features in a grid layout
4. **CTA** - Call-to-action sections
5. **Pricing Table** - Product/service pricing
6. **FAQ** - Accordion-style frequently asked questions
7. **Comparison Table** - Feature comparison tables
8. **Image** - Image blocks with captions
9. **Video** - Embedded video content
10. **Testimonial** - Customer testimonials
11. **Stats** - Statistics and metrics
12. **Contact Form** - Contact forms

## 🔧 API Endpoints

### Content Management
- `GET /marketing/api/pages/` - List all pages
- `GET /marketing/api/posts/` - List all blog posts
- `GET /marketing/api/media/` - List media assets
- `GET /marketing/api/categories/` - List categories
- `GET /marketing/api/tags/` - List tags

### Search
- `GET /marketing/api/search/?q=query` - Search content

### CMS
- `GET /marketing/cms/dashboard/` - CMS dashboard
- `GET /marketing/cms/blocks/builder/` - Block builder interface

## 📱 Responsive Design

The website is fully responsive with breakpoints at:
- Mobile: `< 640px`
- Tablet: `640px - 1023px`
- Desktop: `1024px+`

## 🔍 SEO Features

- **Sitemap**: `/sitemap.xml`
- **Robots.txt**: `/robots.txt`
- **Meta tags** for all pages
- **Open Graph** and **Twitter Card** support
- **Structured data** for rich snippets

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_cms_functionality.py
```

Or use Django's test runner:
```bash
python manage.py test marketing
```

## 🚀 Deployment

### Docker Production Deployment

#### Prerequisites
- Docker and Docker Compose installed on production server
- Environment variables configured
- SSL certificate (for HTTPS)

#### Production Setup

1. **Copy production files to server**
   ```bash
   scp -r beyondcode_project/ user@your-server:/path/to/deployment/
   ```

2. **Create production environment file**
   ```bash
   cp .env.example .env.prod
   # Edit .env.prod with your production values
   ```

3. **Required environment variables for production**
   ```bash
   # Database
   DATABASE_URL=postgresql://user:password@host:port/database
   
   # Security
   SECRET_KEY=your-very-long-secret-key-here
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # Optional services
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   REDIS_URL=redis://localhost:6379/1
   
   # Database credentials
   POSTGRES_PASSWORD=your-secure-password
   ```

4. **Deploy with Docker Compose**
   ```bash
   # Build and start production services
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   
   # Run migrations
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py migrate
   
   # Collect static files
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```

5. **Set up reverse proxy (Nginx)**
   Create `/etc/nginx/sites-available/beyondcode`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location /.well-known/acme-challenge/ {
           root /var/www/certbot;
       }
       
       location / {
           return 301 https://$server_name$request_uri;
       }
   }
   
   server {
       listen 443 ssl;
       server_name yourdomain.com www.yourdomain.com;
       
       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /static/ {
           alias /app/staticfiles/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
       
       location /media/ {
           alias /app/media/;
           expires 1y;
           add_header Cache-Control "public";
       }
   }
   ```

6. **Set up SSL with Let's Encrypt**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Get SSL certificate
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   
   # Set up auto-renewal
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

#### Production Docker Commands

Using Makefile:
```bash
# Deploy to production
make prod-up

# View production logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Run production commands
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Stop production
make prod-down
```

#### Manual Production Deployment

### Production Requirements
- Gunicorn or uWSGI for WSGI server
- Nginx for reverse proxy
- PostgreSQL for production database
- Redis for caching (optional)
- Cloudinary for media storage

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@host:port/db
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Deployment Steps
1. Set up production server
2. Configure environment variables
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Set up WSGI server
6. Configure reverse proxy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test suite for usage examples

## 📊 Performance

The CMS is optimized for performance with:
- **Database optimization** with proper indexing
- **Caching** for frequently accessed content
- **Lazy loading** for images and media
- **Minified assets** in production
- **CDN support** for static files

## 🔐 Security

Security features include:
- **User authentication** and authorization
- **Permission-based access** control
- **CSRF protection** enabled
- **XSS prevention** with proper escaping
- **SQL injection prevention** with ORM
- **Secure headers** configuration

---

**BeyondCode AI** - Powering the future of AI-driven debt collection and compliance solutions.