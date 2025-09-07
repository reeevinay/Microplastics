#!/usr/bin/env python3
"""
Demo script for Microplastic Analysis System
Creates a sample image and tests the analysis pipeline
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw
import os

def create_sample_microplastic_image():
    """Create a sample microplastic image for testing"""
    # Create a 800x600 image with white background
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add some sample "microplastic" particles
    particles = [
        # PE particles (blue-ish)
        {'center': (200, 150), 'size': 30, 'color': (100, 150, 200)},
        {'center': (400, 200), 'size': 25, 'color': (80, 130, 180)},
        
        # PP particles (red-ish)
        {'center': (300, 300), 'size': 35, 'color': (200, 100, 100)},
        {'center': (500, 350), 'size': 28, 'color': (180, 80, 80)},
        
        # PS particles (green-ish)
        {'center': (150, 400), 'size': 32, 'color': (100, 200, 100)},
        {'center': (600, 250), 'size': 26, 'color': (80, 180, 80)},
        
        # PVC particles (purple-ish)
        {'center': (350, 450), 'size': 40, 'color': (150, 100, 200)},
        
        # PET particles (yellow-ish)
        {'center': (250, 100), 'size': 22, 'color': (200, 200, 100)},
        {'center': (550, 400), 'size': 29, 'color': (180, 180, 80)},
    ]
    
    # Draw particles
    for particle in particles:
        x, y = particle['center']
        size = particle['size']
        color = particle['color']
        
        # Draw main particle
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                    fill=color, outline='black', width=2)
        
        # Add some texture/noise
        for i in range(5):
            noise_x = x + np.random.randint(-size//4, size//4)
            noise_y = y + np.random.randint(-size//4, size//4)
            noise_size = np.random.randint(2, 6)
            draw.ellipse([noise_x-noise_size//2, noise_y-noise_size//2, 
                         noise_x+noise_size//2, noise_y+noise_size//2], 
                        fill='black')
    
    # Add some background noise
    for i in range(50):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        size = np.random.randint(1, 3)
        color = tuple(np.random.randint(200, 255) for _ in range(3))
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
    
    # Save the image
    os.makedirs('uploads', exist_ok=True)
    image_path = 'uploads/sample_microplastics.jpg'
    image.save(image_path, 'JPEG', quality=95)
    
    print(f"✓ Created sample image: {image_path}")
    return image_path

def test_analysis_pipeline():
    """Test the analysis pipeline with the sample image"""
    try:
        from microplastic_analyzer import MicroplasticAnalyzer
        from data_comparator import DataComparator
        from solution_recommender import SolutionRecommender
        
        print("\nTesting analysis pipeline...")
        
        # Create sample image
        image_path = create_sample_microplastic_image()
        
        # Initialize components
        analyzer = MicroplasticAnalyzer()
        comparator = DataComparator()
        recommender = SolutionRecommender()
        
        # Analyze the image
        print("Analyzing image...")
        analysis_result = analyzer.analyze_image(image_path)
        
        print(f"✓ Analysis complete:")
        print(f"  - Particles detected: {analysis_result.get('particle_count', 0)}")
        print(f"  - Types found: {len(analysis_result.get('types', []))}")
        print(f"  - Average confidence: {analysis_result.get('average_confidence', 0):.2f}")
        
        # Compare with online data
        print("\nComparing with baseline data...")
        comparison_data = comparator.compare_with_online_data(analysis_result)
        print("✓ Comparison complete")
        
        # Get recommendations
        print("\nGenerating recommendations...")
        recommendations = recommender.get_recommendations(analysis_result, comparison_data)
        print(f"✓ Generated {len(recommendations.get('prevention_solutions', []))} prevention solutions")
        
        print("\n" + "="*50)
        print("DEMO COMPLETE - All components working!")
        print("="*50)
        print("\nTo start the web interface, run:")
        print("python app.py")
        print("\nThen open: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in analysis pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Microplastic Analysis System - Demo")
    print("="*40)
    
    success = test_analysis_pipeline()
    
    if success:
        print("\n✓ Demo completed successfully!")
    else:
        print("\n✗ Demo failed. Please check the error messages above.")
