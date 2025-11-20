# Step-by-Step Render Deployment Guide

Follow these steps **exactly** to deploy your EduVerse project to Render:

## 📋 Prerequisites Checklist

- [ ] GitHub repository is pushed: `https://github.com/ROHIT-THOTA01/EduVerse-Website`
- [ ] All code is committed and pushed to GitHub
- [ ] You have a Render account (or ready to sign up)

---

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Sign Up/Login to Render

1. Go to **https://render.com**
2. Click **"Get Started for Free"** (or **"Log In"** if you already have an account)
3. Sign up using your GitHub account (recommended) or email

---

### Step 2: Create PostgreSQL Database

**Important:** Create the database FIRST before the web service.

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Configure the database:
   - **Name**: `eduverse-db` (or any name you prefer)
   - **Database**: Leave as default or change to `eduverse`
   - **User**: Leave as default
   - **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: Leave as default (latest)
   - **Plan**: Select **"Free"** (or paid if you prefer)
4. Click **"Create Database"**
5. **Wait for database to be ready** (takes 1-2 minutes)
6. Once ready, go to database dashboard and **copy the "Internal Database URL"**
   - It looks like: `postgresql://username:password@hostname/database_name`

---

### Step 3: Create Web Service

1. In Render dashboard, click **"New +"** button again
2. Select **"Web Service"**
3. Connect your repository:
   - If first time: Click **"Connect GitHub"** and authorize Render
   - Select repository: **`ROHIT-THOTA01/EduVerse-Website`**
   - Click **"Connect"**

---

### Step 4: Configure Web Service Settings

Fill in these settings **exactly**:

#### Basic Settings:
- **Name**: `eduverse` (or your preferred name)
- **Environment**: Select **"Python 3"**
- **Region**: Same as your database (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: Leave **empty**

#### Build & Start Commands:
- **Build Command**: 
  ```
  pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
  
- **Start Command**: 
  ```
  gunicorn Coursera.wsgi --log-file -
  ```

---

### Step 5: Add Environment Variables

**Important:** Add these environment variables in the **"Advanced"** section:

1. Click **"Advanced"** at the bottom
2. Scroll to **"Environment Variables"** section
3. Click **"Add Environment Variable"** and add each one:

#### Required Variables:

**1. SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: Generate one using this command (run locally):
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Or use this online tool: https://djecrety.ir/
- **Click "Save Changes"**

**2. DEBUG**
- **Key**: `DEBUG`
- **Value**: `False`
- **Click "Save Changes"**

**3. ALLOWED_HOSTS**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `eduverse.onrender.com` (replace with YOUR actual service name)
  - If your service name is `my-app`, use: `my-app.onrender.com`
- **Click "Save Changes"**

**4. CSRF_TRUSTED_ORIGINS**
- **Key**: `CSRF_TRUSTED_ORIGINS`
- **Value**: `https://eduverse.onrender.com` (replace with YOUR actual service URL)
  - If your service name is `my-app`, use: `https://my-app.onrender.com`
- **Click "Save Changes"**

**5. DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: Paste the **Internal Database URL** you copied in Step 2
  - Should look like: `postgresql://username:password@hostname/database_name`
- **Click "Save Changes"**

#### Optional Variables (if using Stripe):

**6. STRIPE_PUBLISHABLE_KEY**
- **Key**: `STRIPE_PUBLISHABLE_KEY`
- **Value**: Your Stripe publishable key (starts with `pk_`)
- **Click "Save Changes"**

**7. STRIPE_SECRET_KEY**
- **Key**: `STRIPE_SECRET_KEY`
- **Value**: Your Stripe secret key (starts with `sk_`)
- **Click "Save Changes"**

---

### Step 6: Deploy

1. **Double-check** all environment variables are added
2. Scroll to bottom and click **"Create Web Service"**
3. **Wait for deployment** (takes 5-10 minutes)
4. Watch the build logs:
   - Click on your service → **"Logs"** tab
   - You'll see:
     - Installing dependencies
     - Collecting static files
     - Running migrations

---

### Step 7: Run Migrations (After First Deploy)

After the first deployment completes:

1. In your service dashboard, click **"Shell"** tab (or use **"SSH"** link)
2. Run this command:
   ```
   python manage.py migrate
   ```
3. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
   Follow prompts to create admin account

---

### Step 8: Test Your Deployment

1. Once deployment is complete, click **"Live"** link or visit:
   ```
   https://eduverse.onrender.com
   ```
   (Replace with YOUR actual service URL)

2. Test the following:
   - [ ] Home page loads
   - [ ] Sign up works
   - [ ] Login works
   - [ ] Courses page loads
   - [ ] Admin panel works (if you created superuser)

---

## 🔧 Troubleshooting

### Build Fails with "subprocess-exited-with-error"

**Solution:**
1. Check the build logs for specific error
2. Ensure `requirements.txt` has compatible versions
3. Try clearing Render's build cache:
   - Service → **Settings** → **"Clear build cache"**

### Application Crashes on Startup

**Check:**
1. All environment variables are set correctly
2. `DATABASE_URL` is correct and database is running
3. `SECRET_KEY` is set
4. `ALLOWED_HOSTS` matches your service URL

### Static Files Not Loading

**Solution:**
1. Check build logs for `collectstatic` command
2. Verify `whitenoise` is in `requirements.txt`
3. Check `STATIC_ROOT` in `settings.py`

### Database Connection Errors

**Solution:**
1. Verify database is running (green status in Render dashboard)
2. Check `DATABASE_URL` is correct
3. Ensure `psycopg2-binary` is in `requirements.txt`

---

## ✅ Post-Deployment Checklist

- [ ] Application is accessible via URL
- [ ] Database migrations completed
- [ ] Static files loading correctly
- [ ] User registration/login works
- [ ] Admin panel accessible (if superuser created)
- [ ] All pages load without errors

---

## 📝 Important Notes

1. **Free Tier Limitations:**
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - Free PostgreSQL databases delete after 90 days of inactivity

2. **Environment Variables:**
   - Never commit `SECRET_KEY` to GitHub
   - Always use environment variables for sensitive data

3. **Database:**
   - Free tier has data limits
   - Consider upgrading for production use

4. **Media Files:**
   - For production, use cloud storage (AWS S3, Cloudinary)
   - Local storage on Render is ephemeral

---

## 🎉 Success!

Your EduVerse project should now be live on Render! 

If you encounter any issues, check the logs in Render dashboard and refer to the troubleshooting section above.

Good luck! 🚀

