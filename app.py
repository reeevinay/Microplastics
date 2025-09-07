from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
import json
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
from microplastic_analyzer import MicroplasticAnalyzer
from data_comparator import DataComparator
from solution_recommender import SolutionRecommender

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
DATABASE = 'microplastic_analysis.db'

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Initialize components lazily to avoid startup issues
analyzer = None
comparator = None
recommender = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = MicroplasticAnalyzer()
    return analyzer

def get_comparator():
    global comparator
    if comparator is None:
        comparator = DataComparator()
    return comparator

def get_recommender():
    global recommender
    if recommender is None:
        recommender = SolutionRecommender()
    return recommender

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            microplastic_types TEXT,
            confidence_scores TEXT,
            particle_count INTEGER,
            size_distribution TEXT,
            recommendations TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Microplastic Analysis API is running'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze the image
        try:
            analysis_result = get_analyzer().analyze_image(filepath)
            
            # Compare with internet data
            comparison_data = get_comparator().compare_with_online_data(analysis_result)
            
            # Get recommendations
            recommendations = get_recommender().get_recommendations(analysis_result, comparison_data)
            
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_numpy_types(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy_types(item) for item in obj]
                return obj
            
            # Clean all data for JSON serialization
            analysis_result_clean = convert_numpy_types(analysis_result)
            comparison_data_clean = convert_numpy_types(comparison_data)
            recommendations_clean = convert_numpy_types(recommendations)
            
            # Save to database
            save_analysis_to_db(filename, analysis_result_clean, recommendations_clean)
            
            # Generate visualization
            visualization_data = create_visualization(analysis_result_clean)
            
            return jsonify({
                'success': True,
                'analysis': analysis_result_clean,
                'comparison': comparison_data_clean,
                'recommendations': recommendations_clean,
                'visualization': visualization_data
            })
            
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/history')
def get_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analyses ORDER BY analysis_date DESC LIMIT 10')
    results = cursor.fetchall()
    conn.close()
    
    history = []
    for result in results:
        history.append({
            'id': result[0],
            'filename': result[1],
            'date': result[2],
            'microplastic_types': json.loads(result[3]) if result[3] else [],
            'particle_count': result[5]
        })
    
    return jsonify(history)

def save_analysis_to_db(filename, analysis_result, recommendations):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        return obj
    
    # Convert all numpy types before JSON serialization
    analysis_result_clean = convert_numpy_types(analysis_result)
    recommendations_clean = convert_numpy_types(recommendations)
    
    cursor.execute('''
        INSERT INTO analyses (filename, microplastic_types, confidence_scores, 
                            particle_count, size_distribution, recommendations)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        json.dumps(analysis_result_clean.get('types', [])),
        json.dumps(analysis_result_clean.get('confidence_scores', [])),
        int(analysis_result_clean.get('particle_count', 0)),
        json.dumps(analysis_result_clean.get('size_distribution', {})),
        json.dumps(recommendations_clean)
    ))
    conn.commit()
    conn.close()

def create_visualization(analysis_result):
    # Create pie chart for microplastic types
    types = analysis_result.get('types', [])
    counts = analysis_result.get('counts', [])
    
    if not types:
        return None
    
    fig = go.Figure(data=[go.Pie(labels=types, values=counts)])
    fig.update_layout(title="Microplastic Types Distribution")
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
