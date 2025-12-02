# Deployment Guide for Frozen Kashmir

This guide covers deploying your Django website to production so that frozenkashmir.com displays your actual travel website instead of the GoDaddy parking page.

## Deployment Options

Choose one of these hosting providers:

1. **DigitalOcean** - Best for control and scalability
2. **Railway** - Easiest for Django, free tier available
3. **Heroku** - Simple but paid
4. **PythonAnywhere** - Good for beginners
5. **AWS/Google Cloud** - Enterprise-grade but complex

**Recommendation: Railway** (easiest) or **DigitalOcean** (most control)

---

## Option 1: Deploy to Railway (Recommended for Quick Setup)

Railway offers automatic Django deployment with PostgreSQL included.

### Prerequisites
- GitHub account
- Your code pushed to GitHub
- Railway account (free tier available)

### Steps

1. **Prepare Your Code**

   Add a `railway.json` file to your project root:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python manage.py migrate && gunicorn frozenkashmir.wsgi:application",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

   Update `requirements.txt` to include:
   ```
   Django>=5.2
   psycopg2-binary
   gunicorn
   python-dotenv
   Pillow
   ```

   Add `runtime.txt` (optional):
   ```
   python-3.11.0
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin seo-optimization
   ```

3. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click **"Start a New Project"**
   - Choose **"Deploy from GitHub repo"**
   - Select your `FROZENKASHMIR` repository
   - Railway will auto-detect Django and set up PostgreSQL

4. **Configure Environment Variables**

   In Railway dashboard → Variables, add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app,frozenkashmir.com
   FROZENKASHMIR_DB_NAME=railway
   FROZENKASHMIR_DB_USER=postgres
   FROZENKASHMIR_DB_PASSWORD=<auto-provided>
   FROZENKASHMIR_DB_HOST=<auto-provided>
   FROZENKASHMIR_DB_PORT=<auto-provided>
   ```

   **Note:** Database credentials are auto-filled by Railway.

5. **Deploy Static Files**

   Update `settings.py`:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
   
   # For production
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

   Add to `requirements.txt`:
   ```
   whitenoise
   ```

   Update `wsgi.py`:
   ```python
   from django.core.wsgi import get_wsgi_application
   import os
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frozenkashmir.settings')
   
   application = get_wsgi_application()
   ```

   Install and configure WhiteNoise in `settings.py` middleware:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       # ... rest of middleware
   ]
   ```

6. **Get Your Railway URL**
   - Railway will provide a URL like: `your-app.railway.app`
   - Test it to ensure your site works

7. **Point Your Domain**
   - In Railway: Settings → Domains → Add Custom Domain
   - Enter: `frozenkashmir.com`
   - Railway will provide DNS records

   **Update DNS at GoDaddy:**
   - Log in to GoDaddy
   - Go to DNS settings for frozenkashmir.com
   - Add CNAME record:
     - **Type:** CNAME
     - **Name:** `@` or `www`
     - **Value:** `<your-app>.railway.app`
     - **TTL:** 600

   - Wait 10-60 minutes for DNS propagation
   - Your site should be live at frozenkashmir.com!

---

## Option 2: Deploy to DigitalOcean

DigitalOcean provides more control with droplets (virtual servers).

### Prerequisites
- DigitalOcean account ($5/month minimum)
- Basic Linux knowledge

### Quick Setup with App Platform

1. **Create App on DigitalOcean**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Click **Create App**
   - Connect GitHub repository
   - Choose `seo-optimization` branch

2. **Configure Build Settings**
   - **Build Command:** `python manage.py collectstatic --noinput`
   - **Run Command:** `gunicorn frozenkashmir.wsgi:application`
   - **Environment:** Python

3. **Add Database**
   - Click **Add Resource** → **Database**
   - Choose **PostgreSQL**
   - Link to your app

4. **Set Environment Variables**
   (Same as Railway section above)

5. **Add Custom Domain**
   - In App settings → Domains
   - Add `frozenkashmir.com`
   - Update DNS at GoDaddy with provided CNAME

---

## Option 3: Deploy to PythonAnywhere

Good for beginners, includes free tier with limitations.

### Steps

1. **Create Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for free account

2. **Upload Code**
   - Use Git to clone your repository
   - Or upload files manually

3. **Set Up Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to Web tab
   - Add new web app
   - Choose Django
   - Configure WSGI file
   - Set static files path

5. **Set Environment Variables**
   - In Web tab → Environment variables
   - Add your database credentials

6. **Point Domain**
   - Paid accounts only support custom domains
   - Update DNS CNAME to point to your PythonAnywhere subdomain

---

## Post-Deployment Checklist

After deploying to any platform:

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
python manage.py collectstatic
```

### 4. Load Sample Data (if needed)
```bash
python manage.py loaddata initial_data.json
```

### 5. Test Key Endpoints
- Homepage: `https://frozenkashmir.com/`
- Admin: `https://frozenkashmir.com/admin/`
- Sitemap: `https://frozenkashmir.com/sitemap.xml`
- robots.txt: `https://frozenkashmir.com/robots.txt`

### 6. Security Checklist
- [ ] `DEBUG = False` in production
- [ ] Change `SECRET_KEY` from default
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL certificate)
- [ ] Set up CSRF protection
- [ ] Configure secure cookies:
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```

### 7. Configure Media Files
For user-uploaded images (package/destination photos):

**Option A: Use Cloud Storage (Recommended)**
- AWS S3
- DigitalOcean Spaces
- Google Cloud Storage

Install django-storages:
```bash
pip install django-storages boto3
```

**Option B: Serve from Server**
Configure in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Add to `urls.py`:
```python
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Troubleshooting

### Issue: Static files not loading
**Solution:** 
```bash
python manage.py collectstatic --clear
```

### Issue: Database connection error
**Solution:** Check environment variables for database credentials

### Issue: 502 Bad Gateway
**Solution:** Check application logs, ensure gunicorn is running

### Issue: Site still shows GoDaddy page
**Solution:** 
- Check DNS propagation: [dnschecker.org](https://dnschecker.org)
- Clear browser cache
- Wait up to 48 hours for full DNS propagation

---

## Monitoring & Maintenance

### Regular Tasks

1. **Monitor Logs**
   - Check for errors daily
   - Set up log alerts

2. **Database Backups**
   - Enable automated backups on your hosting platform
   - Test restore procedure

3. **Update Dependencies**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

4. **Security Updates**
   - Keep Django updated
   - Monitor security advisories

5. **Performance Monitoring**
   - Use tools like New Relic or Sentry
   - Monitor response times
   - Check database query performance

---

## Recommended Production Settings

Update `settings.py` for production:

```python
import os
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Security settings
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Next Steps

After successful deployment:

1. ✅ Set up Google Search Console (see `GOOGLE_SEARCH_CONSOLE_SETUP.md`)
2. ✅ Submit sitemap to Google
3. ✅ Test all functionality on production
4. ✅ Set up monitoring/alerts
5. ✅ Configure backups
6. ✅ Add SSL certificate (usually automatic on modern platforms)
7. ✅ Test site on mobile devices
8. ✅ Run Lighthouse SEO audit

Your website should now be live and ready for Google indexing! 🚀
