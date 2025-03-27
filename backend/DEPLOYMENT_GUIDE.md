# Quran Khatmah Backend Deployment Guide

This guide explains how to deploy the Quran Khatmah backend to production using PostgreSQL.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- A web hosting service (like PythonAnywhere)
- Access to the shell/terminal

## Deployment Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quran-khatmah
```

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Edit the `.env` file with your production settings:
   ```
   # Django settings
   DJANGO_SECRET_KEY=your-secure-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

   # Database settings
   DB_NAME=quran_khatmah
   DB_USER=super
   DB_PASSWORD=your-strong-password-here
   DB_HOST=Sh3ewit-4454.postgres.pythonanywhere-services.com
   DB_PORT=14454

   # CORS settings
   CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

   - Generate a secure secret key: 
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(50))"
     ```
   - Set `DJANGO_ALLOWED_HOSTS` to your domain names
   - Set the database credentials according to your PostgreSQL setup
   - Set `CORS_ALLOWED_ORIGINS` to the URLs where your frontend is hosted

### 5. Set Up the PostgreSQL Database

1. Create the database:
   ```bash
   cd backend
   python create_db.py
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

### 6. Configure the Web Server (PythonAnywhere Example)

#### PythonAnywhere WSGI Configuration

Create a WSGI configuration file with the following content:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/your-username/quran-khatmah'
if path not in sys.path:
    sys.path.insert(0, path)

path = '/home/your-username/quran-khatmah/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Configure Static Files

In PythonAnywhere's web app configuration:
- Set the URL to `/static/` and the directory to `/home/your-username/quran-khatmah/backend/staticfiles`
- Set the URL to `/media/` and the directory to `/home/your-username/quran-khatmah/backend/media`

### 7. Test the Deployment

Visit your domain (e.g., `https://yourdomain.com/admin`) to ensure the site is running properly.

## Maintenance Tasks

### Database Backup

Regular backups are important. Use PostgreSQL's `pg_dump` utility:

```bash
pg_dump -h Sh3ewit-4454.postgres.pythonanywhere-services.com -p 14454 -U super -d quran_khatmah > backup_$(date +"%Y%m%d").sql
```

### Restoring From Backup

```bash
psql -h Sh3ewit-4454.postgres.pythonanywhere-services.com -p 14454 -U super -d quran_khatmah < backup_file.sql
```

### Updating the Application

1. Pull the latest changes:
   ```bash
   git pull
   ```

2. Install any new dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Apply migrations if needed:
   ```bash
   python manage.py migrate
   ```

4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

5. Restart the web server.

## Troubleshooting

### Connection Issues

If you're having trouble connecting to the database:
- Verify your credentials in the `.env` file
- Check if your IP is allowed to connect to the PostgreSQL server
- Ensure the database service is running

### Permission Errors

If you're experiencing permission issues:
- Check file permissions for media and static files
- Ensure the web server process has appropriate permissions

### 500 Server Errors

If you're seeing 500 errors:
- Check the server logs
- Temporarily set `DEBUG=True` to see detailed error messages (remember to set it back to `False` after debugging)

## Security Considerations

- Keep your `SECRET_KEY` secure and never commit it to version control
- Regularly update your Django and dependencies
- Always use HTTPS in production
- Limit database user permissions to only what is necessary
- Configure proper backup systems
- Set up monitoring for your application 