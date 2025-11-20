# Deploy EduVerse to Vercel (Free) - Step by Step Guide

This guide will help you deploy your Django EduVerse project to Vercel for free.

## ⚠️ Important Notes

**Vercel Limitations:**
- Vercel is primarily designed for frontend/serverless, not traditional Django apps
- Function execution time limit: 10 seconds (Hobby plan), 60 seconds (Pro plan)
- No built-in database (must use external database like Supabase, PlanetScale, etc.)
- Static files are served automatically, but media files need external storage
- SQLite won't work (filesystem is read-only)

**Recommended:** For a production Django app, consider Render or Railway instead. However, Vercel can work for simpler deployments.

---

## 📋 Prerequisites

1. ✅ GitHub repository: `https://github.com/ROHIT-THOTA01/EduVerse-Website`
2. ✅ Vercel account (free): https://vercel.com
3. ✅ External database (free options: Supabase, PlanetScale, Neon, etc.)

---

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Set Up External Database (Required)

Vercel doesn't provide databases. You need an external one:

**Option A: Supabase (Recommended - Free PostgreSQL)**
1. Go to https://supabase.com
2. Sign up for free account
3. Create a new project
4. Go to **Settings** → **Database**
5. Copy the **Connection String** (URI format)

**Option B: PlanetScale (Free MySQL)**
1. Go to https://planetscale.com
2. Sign up for free account
3. Create a new database
4. Copy the connection string

**Option C: Neon (Free PostgreSQL)**
1. Go to https://neon.tech
2. Sign up for free account
3. Create a project
4. Copy the connection string

---

### Step 2: Sign Up/Login to Vercel

1. Go to **https://vercel.com**
2. Click **"Sign Up"** (or **"Log In"**)
3. Sign up with your **GitHub account** (recommended)

---

### Step 3: Install Vercel CLI (Optional but Recommended)

**For Windows (PowerShell):**
```powershell
npm install -g vercel
```

**Verify installation:**
```powershell
vercel --version
```

---

### Step 4: Deploy via Vercel Dashboard (Easiest Method)

1. Go to **https://vercel.com/dashboard**
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository:
   - If not connected: Click **"Connect GitHub Account"** and authorize
   - Search for: **`ROHIT-THOTA01/EduVerse-Website`**
   - Click **"Import"**

---

### Step 5: Configure Project Settings

In the project configuration:

#### Framework Preset:
- **Framework Preset**: Select **"Other"** or **"Django"** (if available)

#### Build & Output Settings:
- **Root Directory**: Leave **empty** (or `.` if required)
- **Build Command**: 
  ```
  pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Output Directory**: Leave **empty**
- **Install Command**: Leave **empty** (handled in build command)

#### Environment Variables:
Click **"Environment Variables"** and add:

**1. SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: Generate one using:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Or use: https://djecrety.ir/

**2. DEBUG**
- **Key**: `DEBUG`
- **Value**: `False`

**3. ALLOWED_HOSTS**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `*.vercel.app` (or your custom domain if you have one)
- Example: `eduverse.vercel.app,eduverse-rohit-thota01.vercel.app`

**4. CSRF_TRUSTED_ORIGINS**
- **Key**: `CSRF_TRUSTED_ORIGINS`
- **Value**: `https://*.vercel.app` (or your custom domain)
- Example: `https://eduverse.vercel.app,https://eduverse-rohit-thota01.vercel.app`

**5. DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: Paste your database connection string from Step 1
  - Supabase format: `postgresql://user:password@host:port/database`
  - PlanetScale format: `mysql://user:password@host:port/database`

**6. VERCEL (Auto-added by Vercel)**
- This is automatically set to `1` when running on Vercel

**7. VERCEL_URL (Auto-added by Vercel)**
- Automatically set to your deployment URL

**Optional - Stripe (if using):**
- **Key**: `STRIPE_PUBLISHABLE_KEY` → Your Stripe publishable key
- **Key**: `STRIPE_SECRET_KEY` → Your Stripe secret key

---

### Step 6: Deploy

1. **Review** all settings
2. Click **"Deploy"**
3. **Wait** for deployment (3-5 minutes)
4. Watch the build logs:
   - Installing dependencies
   - Collecting static files
   - Building functions

---

### Step 7: Run Migrations

After first deployment:

**Option A: Using Vercel Dashboard**
1. Go to your project → **"Functions"** tab
2. Use the function logs to check for errors

**Option B: Using Vercel CLI (Better)**
1. Open terminal in your project directory
2. Run:
   ```bash
   vercel login
   vercel link
   vercel env pull .env.local
   ```

**Option C: Using Database Tool**
1. Connect to your external database
2. Run migrations manually using your database client

**To create superuser:**
You'll need to run this locally with the DATABASE_URL pointing to your production database:
```bash
python manage.py createsuperuser
```

---

### Step 8: Configure Static & Media Files

**Static Files:**
- ✅ Automatically handled by `collectstatic` during build
- Served via Vercel's CDN

**Media Files (User uploads):**
- ⚠️ Vercel's filesystem is read-only
- **Solution**: Use cloud storage:
  - **AWS S3** (free tier available)
  - **Cloudinary** (free tier)
  - **Supabase Storage** (if using Supabase)
  - **Uploadcare** (free tier)

---

## 🛠️ Alternative: Deploy via Vercel CLI

### Step 1: Install Vercel CLI
```powershell
npm install -g vercel
```

### Step 2: Login
```powershell
vercel login
```

### Step 3: Link Project
```powershell
cd "C:\Users\hp\Downloads\Eduverse\Django-Corsera-clone-main"
vercel link
```
- Select or create a project
- Keep default settings

### Step 4: Add Environment Variables
```powershell
vercel env add SECRET_KEY
vercel env add DEBUG
vercel env add ALLOWED_HOSTS
vercel env add CSRF_TRUSTED_ORIGINS
vercel env add DATABASE_URL
```

### Step 5: Deploy
```powershell
vercel --prod
```

---

## 🔧 Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Ensure Python version is compatible (3.9+)

**Error: "Collectstatic failed"**
- Check `STATIC_ROOT` in `settings.py`
- Verify static files directory exists

### Application Crashes

**Error: "Database connection failed"**
- Verify `DATABASE_URL` is correct
- Check database is accessible from internet
- Ensure database firewall allows Vercel IPs

**Error: "DisallowedHost"**
- Add your Vercel URL to `ALLOWED_HOSTS`
- Format: `your-project.vercel.app`

**Error: "CSRF verification failed"**
- Add your Vercel URL to `CSRF_TRUSTED_ORIGINS`
- Format: `https://your-project.vercel.app`

### Function Timeout

**Error: "Function execution exceeded"**
- Vercel Hobby plan: 10-second limit
- Upgrade to Pro plan (60 seconds)
- Or optimize your code/queries

---

## ✅ Post-Deployment Checklist

- [ ] Application loads at Vercel URL
- [ ] Database migrations completed
- [ ] Static files loading correctly
- [ ] User registration works
- [ ] Login works
- [ ] Admin panel accessible (if superuser created)
- [ ] All pages load without errors

---

## 📝 Important Considerations

### Function Execution Time
- **Hobby Plan**: 10 seconds max
- **Pro Plan**: 60 seconds max
- If requests take longer, consider optimizing or using Render/Railway

### Database
- **Must be external** (Supabase, PlanetScale, Neon, etc.)
- **Cannot use SQLite** on Vercel
- Connection pooling recommended for production

### Media Files
- **Cannot store on Vercel** (filesystem is read-only)
- **Must use cloud storage** (S3, Cloudinary, etc.)

### Cost
- **Hobby Plan**: Free (with limitations)
- **Pro Plan**: $20/month (for longer function execution)

---

## 🎯 Recommended Alternatives

If you encounter issues with Vercel, consider:

1. **Render** (Free tier, better for Django)
   - ✅ Built-in PostgreSQL
   - ✅ No function timeout issues
   - ✅ Full Django support
   - See `STEP_BY_STEP_DEPLOY.md`

2. **Railway** (Free tier available)
   - ✅ Easy Django deployment
   - ✅ Built-in database
   - ✅ Simple setup

3. **Fly.io** (Free tier available)
   - ✅ Docker-based
   - ✅ Global deployment
   - ✅ Good for Django

---

## 🎉 Success!

Your EduVerse project should now be live on Vercel!

**Your deployment URL will be:**
```
https://your-project-name.vercel.app
```

If you need help, check the Vercel logs in your dashboard or refer to the troubleshooting section above.

Good luck! 🚀

