import requests
from bs4 import BeautifulSoup
import json
import time
import numpy as np
from datetime import datetime

class DataComparator:
    def __init__(self):
        self.base_urls = {
            'epa': 'https://www.epa.gov/',
            'noaa': 'https://oceanservice.noaa.gov/',
            'who': 'https://www.who.int/',
            'research_papers': 'https://scholar.google.com/'
        }
        
        # Sample data for comparison (in real implementation, this would come from APIs)
        self.baseline_data = {
            'Polyethylene (PE)': {
                'typical_concentration': '15-25%',
                'common_sources': ['Plastic bags', 'Bottles', 'Packaging'],
                'environmental_impact': 'High persistence, bioaccumulation risk',
                'health_effects': 'Potential endocrine disruption'
            },
            'Polypropylene (PP)': {
                'typical_concentration': '10-20%',
                'common_sources': ['Food containers', 'Textiles', 'Ropes'],
                'environmental_impact': 'Moderate persistence',
                'health_effects': 'Limited data on health effects'
            },
            'Polystyrene (PS)': {
                'typical_concentration': '5-15%',
                'common_sources': ['Styrofoam', 'Disposable cups', 'Packaging'],
                'environmental_impact': 'High persistence, breaks into small pieces',
                'health_effects': 'Potential carcinogenic effects'
            },
            'Polyvinyl Chloride (PVC)': {
                'typical_concentration': '3-8%',
                'common_sources': ['Pipes', 'Vinyl flooring', 'Clothing'],
                'environmental_impact': 'High toxicity, difficult to recycle',
                'health_effects': 'Known carcinogen, endocrine disruptor'
            },
            'Polyethylene Terephthalate (PET)': {
                'typical_concentration': '8-18%',
                'common_sources': ['Bottles', 'Clothing', 'Food packaging'],
                'environmental_impact': 'Moderate persistence, recyclable',
                'health_effects': 'Potential leaching of chemicals'
            },
            'Polyamide (Nylon)': {
                'typical_concentration': '2-5%',
                'common_sources': ['Textiles', 'Fishing nets', 'Ropes'],
                'environmental_impact': 'High persistence in marine environments',
                'health_effects': 'Limited research on health effects'
            },
            'Acrylic': {
                'typical_concentration': '1-3%',
                'common_sources': ['Textiles', 'Paints', 'Adhesives'],
                'environmental_impact': 'Moderate persistence',
                'health_effects': 'Potential respiratory irritation'
            }
        }
    
    def compare_with_online_data(self, analysis_result):
        """Compare analysis results with online data sources"""
        try:
            comparison_data = {
                'timestamp': datetime.now().isoformat(),
                'sample_analysis': analysis_result,
                'baseline_comparison': {},
                'trend_analysis': {},
                'risk_assessment': {},
                'data_sources': []
            }
            
            # Compare each detected microplastic type
            for i, microplastic_type in enumerate(analysis_result.get('types', [])):
                if microplastic_type in self.baseline_data:
                    baseline = self.baseline_data[microplastic_type]
                    sample_count = analysis_result.get('counts', [0])[i]
                    total_particles = analysis_result.get('particle_count', 1)
                    sample_percentage = (sample_count / total_particles) * 100
                    
                    comparison_data['baseline_comparison'][microplastic_type] = {
                        'sample_percentage': round(sample_percentage, 2),
                        'typical_range': baseline['typical_concentration'],
                        'common_sources': baseline['common_sources'],
                        'environmental_impact': baseline['environmental_impact'],
                        'health_effects': baseline['health_effects'],
                        'concentration_status': self._assess_concentration(sample_percentage, baseline['typical_concentration'])
                    }
            
            # Perform trend analysis
            comparison_data['trend_analysis'] = self._analyze_trends(analysis_result)
            
            # Risk assessment
            comparison_data['risk_assessment'] = self._assess_risks(analysis_result)
            
            # Add data sources
            comparison_data['data_sources'] = [
                'EPA Microplastics Research',
                'NOAA Marine Debris Program',
                'WHO Environmental Health Guidelines',
                'Scientific Literature Database'
            ]
            
            return comparison_data
            
        except Exception as e:
            print(f"Data comparison failed: {e}")
            return {'error': f'Comparison failed: {str(e)}'}
    
    def _assess_concentration(self, sample_percentage, typical_range):
        """Assess if sample concentration is within typical range"""
        try:
            # Parse typical range (e.g., "15-25%")
            if '-' in typical_range:
                min_val, max_val = map(float, typical_range.replace('%', '').split('-'))
                if min_val <= sample_percentage <= max_val:
                    return 'Normal'
                elif sample_percentage > max_val:
                    return 'Elevated'
                else:
                    return 'Below Average'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def _analyze_trends(self, analysis_result):
        """Analyze trends in the sample"""
        trends = {
            'dominant_type': None,
            'diversity_index': 0,
            'size_distribution': analysis_result.get('size_distribution', {}),
            'overall_assessment': 'Unknown'
        }
        
        types = analysis_result.get('types', [])
        counts = analysis_result.get('counts', [])
        
        if types and counts:
            # Find dominant type
            max_count_idx = counts.index(max(counts))
            trends['dominant_type'] = types[max_count_idx]
            
            # Calculate diversity (simplified Shannon index)
            total = sum(counts)
            if total > 0:
                diversity = -sum((count/total) * np.log(count/total) for count in counts if count > 0)
                trends['diversity_index'] = round(diversity, 3)
            
            # Overall assessment
            if trends['diversity_index'] > 1.5:
                trends['overall_assessment'] = 'High Diversity'
            elif trends['diversity_index'] > 0.5:
                trends['overall_assessment'] = 'Moderate Diversity'
            else:
                trends['overall_assessment'] = 'Low Diversity'
        
        return trends
    
    def _assess_risks(self, analysis_result):
        """Assess environmental and health risks"""
        risk_factors = {
            'high_risk_types': ['Polyvinyl Chloride (PVC)', 'Polystyrene (PS)'],
            'moderate_risk_types': ['Polyethylene (PE)', 'Polypropylene (PP)'],
            'low_risk_types': ['Polyethylene Terephthalate (PET)']
        }
        
        risks = {
            'environmental_risk': 'Low',
            'health_risk': 'Low',
            'risk_factors': [],
            'recommendations': []
        }
        
        types = analysis_result.get('types', [])
        counts = analysis_result.get('counts', [])
        
        high_risk_count = 0
        moderate_risk_count = 0
        
        for i, microplastic_type in enumerate(types):
            count = counts[i] if i < len(counts) else 0
            
            if microplastic_type in risk_factors['high_risk_types']:
                high_risk_count += count
                risks['risk_factors'].append(f"High-risk type detected: {microplastic_type}")
            elif microplastic_type in risk_factors['moderate_risk_types']:
                moderate_risk_count += count
        
        # Assess overall risk
        total_particles = analysis_result.get('particle_count', 1)
        high_risk_percentage = (high_risk_count / total_particles) * 100
        moderate_risk_percentage = (moderate_risk_count / total_particles) * 100
        
        if high_risk_percentage > 20:
            risks['environmental_risk'] = 'High'
            risks['health_risk'] = 'High'
        elif high_risk_percentage > 10 or moderate_risk_percentage > 50:
            risks['environmental_risk'] = 'Moderate'
            risks['health_risk'] = 'Moderate'
        
        return risks
    
    def fetch_latest_research(self, microplastic_type):
        """Fetch latest research data for a specific microplastic type"""
        try:
            # In a real implementation, this would query research databases
            # For now, return sample data
            research_data = {
                'recent_studies': [
                    {
                        'title': f'Environmental Impact of {microplastic_type}',
                        'year': 2023,
                        'journal': 'Environmental Science & Technology',
                        'key_findings': 'Study shows significant environmental persistence'
                    }
                ],
                'regulatory_updates': [
                    {
                        'region': 'EU',
                        'regulation': 'Single Use Plastics Directive',
                        'status': 'Active',
                        'impact': 'Restricts certain plastic products'
                    }
                ]
            }
            return research_data
        except Exception as e:
            print(f"Research data fetch failed: {e}")
            return {'error': f'Failed to fetch research data: {str(e)}'}
