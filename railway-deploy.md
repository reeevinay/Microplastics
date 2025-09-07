# Railway Deployment Guide

## Deploy to Railway (Modern Heroku Alternative)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your repository

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your microplastic analyzer repository
4. Railway will automatically detect it's a Python app

### Step 3: Configure Environment
```bash
# In Railway dashboard, add these environment variables:
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Step 4: Deploy
Railway will automatically build and deploy your app!

### Benefits of Railway:
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in database support
- ✅ Custom domains
- ✅ Better free tier than Heroku

Your app will be live at: `https://your-app-name.railway.app`
