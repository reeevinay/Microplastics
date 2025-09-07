# Microplastic Analysis System

An advanced AI-powered system for analyzing microplastic images from emission microscopy and providing actionable solutions for environmental protection.

## Features

- **AI-Powered Image Analysis**: Uses pre-trained machine learning models to identify different types of microplastics
- **Real-time Data Comparison**: Compares analysis results with global databases and research findings
- **Actionable Recommendations**: Provides personalized solutions for microplastic reduction and prevention
- **Interactive Web Interface**: Modern, responsive web application for easy image upload and result visualization
- **Analysis History**: Tracks and stores previous analyses for comparison and trend analysis

## Supported Microplastic Types

- Polyethylene (PE)
- Polypropylene (PP)
- Polystyrene (PS)
- Polyvinyl Chloride (PVC)
- Polyethylene Terephthalate (PET)
- Polyamide (Nylon)
- Acrylic
- Unknown/Other

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd microplastic-analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Web Interface

1. **Upload Image**: Drag and drop or click to upload an emission microscopy image
2. **Analyze**: Click the "Analyze Image" button to start the AI analysis
3. **View Results**: Review the analysis results including:
   - Particle count and types
   - Size distribution
   - Risk assessment
   - Comparison with baseline data
4. **Get Recommendations**: Access personalized solutions for microplastic reduction

### API Endpoints

- `POST /upload`: Upload and analyze an image
- `GET /history`: Retrieve analysis history

## System Architecture

### Components

1. **MicroplasticAnalyzer**: Core AI model for image analysis and particle classification
2. **DataComparator**: Compares results with online databases and research
3. **SolutionRecommender**: Generates personalized recommendations
4. **Web Interface**: Flask-based frontend for user interaction

### Database

The system uses SQLite to store:
- Analysis results
- Particle classifications
- Confidence scores
- Recommendations
- Timestamps

## Technical Details

### Image Processing Pipeline

1. **Preprocessing**: Image resizing, normalization, and format conversion
2. **Particle Detection**: Contour detection and particle isolation
3. **Classification**: AI model prediction for each detected particle
4. **Post-processing**: Result aggregation and confidence scoring

### AI Model

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 224x224 pixels
- **Classes**: 8 microplastic types
- **Framework**: TensorFlow/Keras

## File Structure

```
microplastic-analyzer/
├── app.py                      # Main Flask application
├── microplastic_analyzer.py    # Core analysis engine
├── data_comparator.py          # Data comparison module
├── solution_recommender.py     # Recommendation system
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface template
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── images/                # Static images
├── uploads/                   # Uploaded images
├── results/                   # Analysis results
└── models/                    # AI model files
```

## Configuration

### Environment Variables

- `FLASK_ENV`: Set to 'development' for debug mode
- `UPLOAD_FOLDER`: Directory for uploaded images (default: 'uploads')
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 10MB)

### Model Configuration

The system automatically creates a demo model if no pre-trained model is found. For production use, replace the demo model with a properly trained model.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.

## Future Enhancements

- Integration with real-time research databases
- Advanced visualization tools
- Batch processing capabilities
- Mobile application
- API for third-party integrations
- Enhanced AI models with more microplastic types
