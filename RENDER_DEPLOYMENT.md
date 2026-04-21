# Render Deployment Guide

## Fixed Issues in Your Django Configuration

The following issues were corrected to fix the internal server error:

### 1. **Database Configuration** ✅
- **Problem**: Database URL handling was causing connection failures
- **Fix**: Added proper fallback logic to handle missing `DATABASE_URL` environment variable

### 2. **Logging Configuration** ✅
- **Added**: Comprehensive logging setup to diagnose errors in production
- **Benefit**: All errors will now be visible in Render's logs for debugging

### 3. **Security Headers** ✅
- **Added**: HTTPS redirect, secure cookies, XSS protection
- **Note**: Only active when `DEBUG = False` (which it is)

### 4. **Timezone Configuration** ✅
- **Set**: UTC timezone with timezone support enabled

## Required Render Environment Variables

You MUST set these in your Render dashboard under "Environment":

1. **DATABASE_URL** (Required)
   - Format: `postgresql://user:password@host:port/database`
   - Get this from your PostgreSQL service on Render

2. **SECRET_KEY** (Required)
   - Generate a random secret key (32+ characters)
   - Example: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

3. **DJANGO_LOG_LEVEL** (Optional, default: INFO)
   - Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Render Deployment Steps

1. Push your code to GitHub (make sure `build.sh` is included)

2. In Render Dashboard:
   - Create new Web Service
   - Connect your GitHub repository
   - Set Runtime: Python 3.11
   - Set Build Command: `./build.sh`
   - Set Start Command: `cd pharmacy && gunicorn pharmacy.wsgi:application`

3. Add Environment Variables (as listed above)

4. Connect PostgreSQL database:
   - Create or link PostgreSQL instance
   - Render will automatically set `DATABASE_URL`

5. Deploy and check logs

## Testing Locally Before Deploying

Run these commands in your pharmacy folder:

```bash
# Set environment variables
$env:DEBUG = "False"
$env:DATABASE_URL = "postgresql://localhost/pharmacy_test"
$env:SECRET_KEY = "your-secret-key-here"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Test with gunicorn
gunicorn pharmacy.wsgi:application
```

## If You Still Get Errors

Check Render logs:
1. Go to your service in Render dashboard
2. Click "Logs" tab
3. Look for any Python errors or stack traces
4. Common issues:
   - Missing migrations: Run `python manage.py migrate`
   - Missing dependencies: Ensure requirements.txt has all packages
   - Database connection: Verify `DATABASE_URL` is correct

## Static Files Note

- WhiteNoise is configured to serve static files
- If you have an admin interface, it will be available at `/admin/`
- No additional CDN or static file server needed
