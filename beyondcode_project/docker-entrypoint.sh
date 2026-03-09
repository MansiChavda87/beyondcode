#!/bin/bash
set -e

# Wait for database to be ready
if [ "$DATABASE_URL" ]; then
    echo "Waiting for database to be ready..."
    until pg_isready -h db -p 5432 -U postgres; do
      echo "Database is unavailable - sleeping"
      sleep 2
    done
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if not exists (for development)
if [ "$DEBUG" = "True" ]; then
    echo "Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
fi

# Seed initial content if requested
if [ "$SEED_DATA" = "True" ]; then
    echo "Seeding initial content..."
    python manage.py seed_cms_content
    python manage.py seed_cms_admin
fi

# Execute the command passed in
exec "$@"