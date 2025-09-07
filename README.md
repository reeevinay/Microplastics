# Microplastic Analysis System

A web-based application for analyzing microplastic contamination in emission microscopy images using AI-powered detection and analysis.

## 🌟 Features

- **AI-Powered Analysis**: Advanced machine learning models for microplastic identification
- **Interactive Visualization**: Real-time charts and graphs showing analysis results
- **Comprehensive Reports**: Detailed analysis with recommendations and solutions
- **History Tracking**: Keep track of all your analyses
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Live Demo

Visit the live application: [https://your-username.github.io/Sensor](https://your-username.github.io/Sensor)

## 📱 How to Use

1. **Upload Image**: Drag and drop or click to upload an emission microscopy image
2. **Analyze**: Click "Analyze Image" to start the AI-powered analysis
3. **View Results**: See detailed analysis including:
   - Particle count and types
   - Size distribution charts
   - Risk assessment
   - Actionable recommendations
4. **Track History**: View all your previous analyses

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Charts**: Plotly.js
- **Icons**: Font Awesome
- **Storage**: LocalStorage for demo data

## 📁 Project Structure

```
├── index.html              # Main application page
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   ├── js/
│   │   └── app.js          # Main application logic
│   └── images/             # Static images
├── templates/              # Flask templates (for backend version)
├── app.py                  # Flask backend (for full version)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Setup for GitHub Pages

1. **Fork this repository**
2. **Enable GitHub Pages**:
   - Go to your repository settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

3. **Your site will be available at**:
   `https://your-username.github.io/Sensor`

## 🎯 Demo Mode

This GitHub Pages version runs in **demo mode** with simulated analysis results. The application:

- ✅ **Fully functional UI** - All features work perfectly
- ✅ **Realistic demo data** - Generates realistic microplastic analysis results
- ✅ **Interactive charts** - Plotly.js visualizations work completely
- ✅ **History tracking** - Uses localStorage to save analysis history
- ✅ **Responsive design** - Works on all devices

## 🔬 Analysis Features

### Detected Microplastic Types
- Polyethylene (PE)
- Polypropylene (PP)
- Polystyrene (PS)
- Polyvinyl Chloride (PVC)
- Polyethylene Terephthalate (PET)
- Nylon
- Acrylic

### Analysis Results Include
- **Particle Count**: Total number of microplastics detected
- **Type Distribution**: Pie chart showing types found
- **Size Distribution**: Bar chart showing particle sizes
- **Risk Assessment**: Environmental risk level (Low/Medium/High)
- **Confidence Scores**: AI confidence in detection accuracy

### Recommendations
- **Prevention Solutions**: Actionable steps to reduce microplastics
- **Implementation Plans**: Timeline for implementing solutions
- **Cost Analysis**: Cost and effectiveness ratings

## 🌐 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## 📱 Mobile Support

- ✅ Responsive design
- ✅ Touch-friendly interface
- ✅ Optimized charts for mobile
- ✅ Fast loading on mobile networks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap for the responsive UI framework
- Plotly.js for interactive charts
- Font Awesome for icons
- The scientific community for microplastic research

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/Sensor/issues) page
2. Create a new issue with detailed description
3. Include screenshots if applicable

---

**Note**: This is a demo version for GitHub Pages. For full AI analysis capabilities, the complete Python backend with TensorFlow models is available in the `app_full.py` file.