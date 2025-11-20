# Render Deployment Guide for EduVerse

This guide will help you deploy your Django EduVerse project to Render.

## Prerequisites

1. A GitHub account with your repository: `https://github.com/ROHIT-THOTA01/EduVerse-Website`
2. A Render account (free tier available): https://render.com

## Step-by-Step Deployment Instructions

### 1. Sign up for Render

- Go to https://render.com and sign up for a free account
- You can sign up with your GitHub account for easier integration

### 2. Create a New Web Service

1. Click **"New +"** button in the Render dashboard
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select the repository: **`ROHIT-THOTA01/EduVerse-Website`**
5. Click **"Connect"**

### 3. Configure Web Service Settings

Use these settings:

- **Name**: `eduverse` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose the closest region to your users
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn Coursera.wsgi --log-file -
  ```

### 4. Add Environment Variables

Click **"Advanced"** and add these environment variables:

#### Required Variables:

1. **SECRET_KEY**
   - Generate a new Django secret key:
     ```python
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   - Copy the generated key and paste it as the value

2. **DEBUG**: `False`

3. **ALLOWED_HOSTS**: 
   - Your Render service URL (e.g., `eduverse.onrender.com`)
   - You can add multiple hosts separated by commas

4. **CSRF_TRUSTED_ORIGINS**: 
   - `https://eduverse.onrender.com` (replace with your actual URL)

#### Optional Variables (for Stripe payments):

5. **STRIPE_PUBLISHABLE_KEY**: Your Stripe publishable key
6. **STRIPE_SECRET_KEY**: Your Stripe secret key

#### Database Variable (Auto-created):

7. **DATABASE_URL**: This will be automatically created when you add a database (see step 5)

### 5. Add PostgreSQL Database

1. Go back to Render dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `eduverse-db`
   - **Plan**: `Free` (or choose a paid plan)
   - **Region**: Same as your web service
4. Click **"Create Database"**
5. Copy the **Internal Database URL** from the database dashboard
6. Go back to your Web Service settings
7. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from step 5

### 6. Update render.yaml (Optional - for automated setup)

The `render.yaml` file is already in your repository. If you want to use it:

1. In Render dashboard, go to **"Blueprints"**
2. Click **"New Blueprint Instance"**
3. Select your repository
4. Render will automatically detect `render.yaml` and create all services

### 7. Deploy

1. Click **"Create Web Service"** (or **"Apply"** if using Blueprint)
2. Render will start building and deploying your application
3. Wait for the build to complete (this may take 5-10 minutes)
4. Once deployed, your app will be live at: `https://eduverse.onrender.com`

### 8. Run Migrations

After first deployment, you need to run migrations:

1. Go to your Web Service dashboard in Render
2. Click on **"Shell"** tab (or use the terminal in Render dashboard)
3. Run:
   ```
   python manage.py migrate
   ```
4. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

## Post-Deployment Checklist

- [ ] Database migrations completed
- [ ] Static files collected (done automatically in build command)
- [ ] Superuser created (if needed)
- [ ] Environment variables set correctly
- [ ] Test the deployed application
- [ ] Verify Stripe integration (if using)
- [ ] Check logs for any errors

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility

### Application Crashes

- Check the logs tab in Render dashboard
- Verify all environment variables are set
- Ensure `DATABASE_URL` is correctly configured
- Check `ALLOWED_HOSTS` includes your Render URL

### Static Files Not Loading

- Verify `collectstatic` runs in build command
- Check `STATIC_ROOT` in settings.py
- Ensure WhiteNoise middleware is enabled (already added)

### Database Connection Errors

- Verify `DATABASE_URL` environment variable is set
- Check database is running (in Render dashboard)
- Ensure `psycopg2-binary` is in requirements.txt (already added)

## Important Notes

1. **Free Tier Limitations**: 
   - Render free tier services spin down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds to wake up

2. **Database**: 
   - Free PostgreSQL databases are deleted after 90 days of inactivity
   - Consider upgrading for production use

3. **Media Files**: 
   - For production, use cloud storage (AWS S3, Cloudinary, etc.) for user-uploaded media files
   - Local storage on Render is ephemeral

4. **Secret Key**: 
   - Never commit your production `SECRET_KEY` to GitHub
   - Always use environment variables for sensitive data

## Next Steps

1. Set up a custom domain (optional)
2. Configure email backend for password resets
3. Set up monitoring and logging
4. Configure backups for your database
5. Add cloud storage for media files

## Support

- Render Documentation: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

Good luck with your deployment! 🚀

