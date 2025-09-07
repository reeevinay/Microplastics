"""
Configuration settings for Microplastic Analysis System
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'microplastic-analysis-secret-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    
    # Database settings
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'microplastic_analysis.db')
    
    # Model settings
    MODEL_PATH = os.environ.get('MODEL_PATH', 'models/microplastic_model.h5')
    INPUT_SIZE = (224, 224)
    
    # Analysis settings
    MIN_PARTICLE_AREA = int(os.environ.get('MIN_PARTICLE_AREA', 50))
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', 0.5))
    
    # API settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with production settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-this'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 5 * 1024 * 1024))  # 5MB for production

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
