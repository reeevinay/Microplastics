# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup (Optional)
```bash
python setup.py
```

### 3. Start the Application
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

## 🧪 Test the System
```bash
python demo.py
```

## 📁 Project Structure
```
Sensor/
├── app.py                 # Main Flask application
├── microplastic_analyzer.py    # AI analysis engine
├── data_comparator.py          # Data comparison module
├── solution_recommender.py     # Recommendation system
├── templates/index.html        # Web interface
├── static/                     # CSS, JS, images
├── requirements.txt            # Dependencies
└── README.md                   # Full documentation
```

## 🔧 Features

- **AI-Powered Analysis**: Identifies 8 types of microplastics
- **Real-time Comparison**: Compares with global databases
- **Actionable Solutions**: Personalized recommendations
- **Interactive Web UI**: Modern, responsive interface
- **Analysis History**: Track previous analyses

## 🎯 How to Use

1. **Upload Image**: Drag & drop or click to upload emission microscopy image
2. **Analyze**: Click "Analyze Image" to start AI processing
3. **View Results**: See particle count, types, and risk assessment
4. **Get Solutions**: Access personalized recommendations

## 🆘 Troubleshooting

- **Import Errors**: Run `pip install -r requirements.txt`
- **Port Issues**: Change port in `app.py` (line with `app.run()`)
- **File Upload Issues**: Check file size (max 10MB) and format (images only)

## 📞 Support

See `README.md` for detailed documentation and troubleshooting.
