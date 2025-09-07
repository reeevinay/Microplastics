import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import json
import os

class MicroplasticAnalyzer:
    def __init__(self):
        # Microplastic type definitions
        self.microplastic_types = {
            0: "Polyethylene (PE)",
            1: "Polypropylene (PP)", 
            2: "Polystyrene (PS)",
            3: "Polyvinyl Chloride (PVC)",
            4: "Polyethylene Terephthalate (PET)",
            5: "Polyamide (Nylon)",
            6: "Acrylic",
            7: "Unknown/Other"
        }
        
        self.model = None
        self.load_model()
        
        # Size categories
        self.size_categories = {
            'small': (0, 100),      # 0-100 micrometers
            'medium': (100, 500),   # 100-500 micrometers  
            'large': (500, 1000)    # 500-1000 micrometers
        }
    
    def load_model(self):
        """Load or create a pre-trained model for microplastic classification"""
        try:
            # Try to load existing model
            if os.path.exists('models/microplastic_model.h5'):
                self.model = tf.keras.models.load_model('models/microplastic_model.h5')
                print("Loaded existing microplastic classification model")
            else:
                # Create a simple CNN model for demonstration
                self.create_demo_model()
                print("Created demo model for microplastic classification")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.create_demo_model()
    
    def create_demo_model(self):
        """Create a demo CNN model for microplastic classification"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.microplastic_types), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the demo model
        self.model.save('models/microplastic_model.h5')
    
    def preprocess_image(self, image_path):
        """Preprocess image for analysis"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size
            image = cv2.resize(image, (224, 224))
            
            # Normalize pixel values
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
        except Exception as e:
            raise ValueError(f"Image preprocessing failed: {e}")
    
    def detect_particles(self, image_path):
        """Detect microplastic particles in the image with improved accuracy"""
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Enhanced preprocessing
            # Apply bilateral filter to reduce noise while preserving edges
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Apply adaptive threshold for better particle detection
            thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Morphological operations to clean up the image
            kernel = np.ones((3,3), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            # Find contours with hierarchy
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            particles = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # More sophisticated filtering
                if area > 30:  # Minimum area threshold
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate aspect ratio to filter out very elongated objects
                    aspect_ratio = float(w) / h
                    if 0.1 < aspect_ratio < 10:  # Reasonable aspect ratio
                        
                        # Calculate more accurate size
                        # Assuming 1 pixel = 1 micrometer (adjust based on your microscope)
                        size_micrometers = max(w, h)
                        
                        # Calculate circularity to identify round particles
                        perimeter = cv2.arcLength(contour, True)
                        if perimeter > 0:
                            circularity = 4 * np.pi * area / (perimeter * perimeter)
                        else:
                            circularity = 0
                        
                        # Calculate solidity (convex hull ratio)
                        hull = cv2.convexHull(contour)
                        hull_area = cv2.contourArea(hull)
                        solidity = float(area) / hull_area if hull_area > 0 else 0
                        
                        particles.append({
                            'contour': contour,
                            'area': area,
                            'size_micrometers': size_micrometers,
                            'bbox': (x, y, w, h),
                            'circularity': circularity,
                            'solidity': solidity,
                            'aspect_ratio': aspect_ratio
                        })
            
            return particles
        except Exception as e:
            print(f"Particle detection failed: {e}")
            return []
    
    def classify_particle(self, image, particle_data):
        """Classify a single particle with enhanced features"""
        try:
            x, y, w, h = particle_data['bbox']
            
            # Extract particle region with padding
            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)
            
            particle_img = image[y1:y2, x1:x2]
            
            # Enhanced preprocessing
            # Convert to RGB if needed
            if len(particle_img.shape) == 3:
                particle_img = cv2.cvtColor(particle_img, cv2.COLOR_BGR2RGB)
            
            # Apply histogram equalization for better contrast
            if len(particle_img.shape) == 3:
                # For color images, equalize each channel
                for i in range(3):
                    particle_img[:,:,i] = cv2.equalizeHist(particle_img[:,:,i])
            else:
                particle_img = cv2.equalizeHist(particle_img)
            
            # Resize to model input size
            particle_img = cv2.resize(particle_img, (224, 224))
            
            # Normalize
            particle_img = particle_img.astype(np.float32) / 255.0
            
            # Add batch dimension
            particle_img = np.expand_dims(particle_img, axis=0)
            
            # Predict
            predictions = self.model.predict(particle_img, verbose=0)
            class_id = np.argmax(predictions[0])
            confidence = float(predictions[0][class_id])
            
            # Apply confidence threshold
            if confidence < 0.3:  # Low confidence threshold
                class_id = 7  # Unknown/Other
                confidence = 0.3
            
            # Get all prediction scores for analysis
            all_scores = [float(score) for score in predictions[0]]
            
            return {
                'type': self.microplastic_types[class_id],
                'confidence': confidence,
                'class_id': class_id,
                'all_scores': all_scores,
                'particle_features': {
                    'circularity': particle_data.get('circularity', 0),
                    'solidity': particle_data.get('solidity', 0),
                    'aspect_ratio': particle_data.get('aspect_ratio', 1)
                }
            }
        except Exception as e:
            print(f"Particle classification failed: {e}")
            return {
                'type': 'Unknown/Other',
                'confidence': 0.0,
                'class_id': 7,
                'all_scores': [0.0] * len(self.microplastic_types),
                'particle_features': {}
            }
    
    def analyze_image(self, image_path):
        """Main analysis function"""
        try:
            # Load original image
            original_image = cv2.imread(image_path)
            if original_image is None:
                raise ValueError("Could not load image")
            
            # Detect particles
            particles = self.detect_particles(image_path)
            
            if not particles:
                return {
                    'types': [],
                    'counts': [],
                    'confidence_scores': [],
                    'particle_count': 0,
                    'size_distribution': {},
                    'particles': []
                }
            
            # Classify each particle
            classified_particles = []
            type_counts = {}
            confidence_scores = []
            
            for particle in particles:
                classification = self.classify_particle(original_image, particle)
                
                particle_info = {
                    'size_micrometers': particle['size_micrometers'],
                    'area': particle['area'],
                    'classification': classification,
                    'circularity': particle.get('circularity', 0),
                    'solidity': particle.get('solidity', 0),
                    'aspect_ratio': particle.get('aspect_ratio', 1)
                }
                classified_particles.append(particle_info)
                
                # Count types
                particle_type = classification['type']
                if particle_type in type_counts:
                    type_counts[particle_type] += 1
                else:
                    type_counts[particle_type] = 1
                
                confidence_scores.append(classification['confidence'])
            
            # Calculate size distribution
            size_distribution = self.calculate_size_distribution(classified_particles)
            
            # Prepare results
            types = list(type_counts.keys())
            counts = list(type_counts.values())
            
            return {
                'types': types,
                'counts': counts,
                'confidence_scores': [float(score) for score in confidence_scores],
                'particle_count': int(len(particles)),
                'size_distribution': size_distribution,
                'particles': classified_particles,
                'average_confidence': float(np.mean(confidence_scores)) if confidence_scores else 0.0
            }
            
        except Exception as e:
            raise ValueError(f"Image analysis failed: {e}")
    
    def calculate_size_distribution(self, particles):
        """Calculate size distribution of particles"""
        distribution = {'small': 0, 'medium': 0, 'large': 0}
        
        for particle in particles:
            size = particle['size_micrometers']
            if size < 100:
                distribution['small'] += 1
            elif size < 500:
                distribution['medium'] += 1
            else:
                distribution['large'] += 1
        
        return distribution
