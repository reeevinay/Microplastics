# GitHub Pages Deployment Guide

## Option 1: Static Frontend Only (GitHub Pages)

### Step 1: Create a Static Version
```bash
# Create a static version of your frontend
mkdir static-site
cp -r templates/ static-site/
cp -r static/ static-site/
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Add static site for GitHub Pages"
git push origin main
```

### Step 3: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll to "Pages" section
4. Select "Deploy from a branch"
5. Choose "main" branch and "/ (root)" folder
6. Click "Save"

Your site will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

**Note:** This only shows the frontend. The AI analysis won't work without a backend.
