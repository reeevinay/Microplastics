# Deployment Guide for Microplastic Analysis System

## 🚀 **GitHub Deployment**

### **Step 1: Prepare for GitHub**
```bash
# Run the deployment script
python deploy.py
```

### **Step 2: Create GitHub Repository**
1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it something like `microplastic-analyzer` or `microplastic-analysis-system`
3. Make it public or private based on your needs

### **Step 3: Connect to GitHub**
```bash
# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## 👥 **Team Setup Instructions**

### **For Team Members to Get Started:**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Web Interface**
   Open browser to: `http://localhost:5000`

## 🔧 **Production Deployment Options**

### **Option 1: Heroku (Recommended for Teams)**
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### **Option 2: Docker Deployment**
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t microplastic-analyzer .
docker run -p 5000:5000 microplastic-analyzer
```

### **Option 3: Local Network Sharing**
For team access on local network:
```bash
# Run with network access
python app.py
```
Then team members can access via: `http://YOUR_IP:5000`

## 📁 **File Structure for Team**
```
microplastic-analyzer/
├── app.py                    # Main application
├── microplastic_analyzer.py  # AI analysis engine
├── data_comparator.py        # Data comparison
├── solution_recommender.py   # Recommendations
├── templates/index.html      # Web interface
├── static/                   # CSS, JS, images
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── DEPLOYMENT.md             # This file
└── .gitignore               # Git ignore rules
```

## 🔒 **Security Considerations**

1. **Environment Variables**: Use `.env` files for sensitive data
2. **File Upload Limits**: Configured in `config.py`
3. **Database Security**: SQLite is local-only by default
4. **Network Access**: Only expose to trusted networks

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Dependencies Missing**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Permission Errors**
   ```bash
   # On Windows
   python -m pip install --user -r requirements.txt
   ```

4. **Model Loading Issues**
   - The system will create a demo model automatically
   - For production, replace with a trained model

## 📊 **Performance Optimization**

1. **For Large Images**: Resize before upload
2. **For Multiple Users**: Use a production server (Gunicorn)
3. **For Better Accuracy**: Train the model with your specific data

## 🔄 **Updates and Maintenance**

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```

2. **Database Backup**
   ```bash
   cp microplastic_analysis.db backup_$(date +%Y%m%d).db
   ```

3. **Log Monitoring**
   - Check console output for errors
   - Monitor upload folder size

## 📞 **Support**

- Check `README.md` for detailed documentation
- Review `QUICKSTART.md` for quick setup
- Open issues on GitHub for bugs
- Contact team lead for technical support
