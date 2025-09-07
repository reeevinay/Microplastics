# Heroku Deployment Guide

## Deploy Your Microplastic Analysis System to Heroku

### Prerequisites
1. GitHub repository with your code
2. Heroku account (free at heroku.com)
3. Heroku CLI installed

### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use package manager:
# Windows: choco install heroku
# Mac: brew install heroku
# Linux: snap install heroku
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
# Create a new Heroku app
heroku create your-microplastic-analyzer

# Or create with a specific name
heroku create microplastic-analysis-system
```

### Step 4: Set Environment Variables
```bash
# Set Flask environment
heroku config:set FLASK_ENV=production

# Set secret key
heroku config:set SECRET_KEY=your-secret-key-here
```

### Step 5: Deploy to Heroku
```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/your-app-name.git

# Deploy
git push heroku main
```

### Step 6: Open Your App
```bash
heroku open
```

### Your app will be live at:
`https://your-app-name.herokuapp.com`

## Free Tier Limitations
- App sleeps after 30 minutes of inactivity
- 550-1000 free dyno hours per month
- Perfect for demos and testing

## Upgrade Options
- Hobby tier ($7/month): Always-on, custom domains
- Professional tier ($25/month): Better performance

## Troubleshooting
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart
```
