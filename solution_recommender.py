import json
from datetime import datetime

class SolutionRecommender:
    def __init__(self):
        self.solution_database = {
            'prevention': {
                'Polyethylene (PE)': [
                    {
                        'solution': 'Use reusable bags and containers',
                        'effectiveness': 'High',
                        'implementation': 'Easy',
                        'cost': 'Low',
                        'description': 'Replace single-use plastic bags with reusable alternatives'
                    },
                    {
                        'solution': 'Support plastic bag bans',
                        'effectiveness': 'Very High',
                        'implementation': 'Medium',
                        'cost': 'Medium',
                        'description': 'Advocate for local plastic bag ban legislation'
                    }
                ],
                'Polypropylene (PP)': [
                    {
                        'solution': 'Choose glass or metal food containers',
                        'effectiveness': 'High',
                        'implementation': 'Easy',
                        'cost': 'Medium',
                        'description': 'Replace PP food containers with more sustainable alternatives'
                    },
                    {
                        'solution': 'Support extended producer responsibility',
                        'effectiveness': 'High',
                        'implementation': 'Hard',
                        'cost': 'High',
                        'description': 'Advocate for policies that make producers responsible for end-of-life products'
                    }
                ],
                'Polystyrene (PS)': [
                    {
                        'solution': 'Ban styrofoam products',
                        'effectiveness': 'Very High',
                        'implementation': 'Medium',
                        'cost': 'Medium',
                        'description': 'Support local bans on polystyrene foam products'
                    },
                    {
                        'solution': 'Use biodegradable alternatives',
                        'effectiveness': 'High',
                        'implementation': 'Easy',
                        'cost': 'Medium',
                        'description': 'Choose biodegradable packaging materials'
                    }
                ],
                'Polyvinyl Chloride (PVC)': [
                    {
                        'solution': 'Avoid PVC products',
                        'effectiveness': 'Very High',
                        'implementation': 'Easy',
                        'cost': 'Low',
                        'description': 'Choose alternatives to PVC pipes, flooring, and clothing'
                    },
                    {
                        'solution': 'Support PVC phase-out policies',
                        'effectiveness': 'Very High',
                        'implementation': 'Hard',
                        'cost': 'High',
                        'description': 'Advocate for regulatory phase-out of PVC products'
                    }
                ],
                'Polyethylene Terephthalate (PET)': [
                    {
                        'solution': 'Improve recycling infrastructure',
                        'effectiveness': 'High',
                        'implementation': 'Medium',
                        'cost': 'High',
                        'description': 'Support better PET recycling programs and facilities'
                    },
                    {
                        'solution': 'Use refillable containers',
                        'effectiveness': 'High',
                        'implementation': 'Easy',
                        'cost': 'Low',
                        'description': 'Choose refillable water bottles and containers'
                    }
                ],
                'Polyamide (Nylon)': [
                    {
                        'solution': 'Use natural fiber alternatives',
                        'effectiveness': 'High',
                        'implementation': 'Easy',
                        'cost': 'Medium',
                        'description': 'Choose cotton, wool, or other natural fibers over nylon'
                    },
                    {
                        'solution': 'Support fishing gear recovery programs',
                        'effectiveness': 'High',
                        'implementation': 'Medium',
                        'cost': 'Medium',
                        'description': 'Participate in or support programs that recover lost fishing gear'
                    }
                ],
                'Acrylic': [
                    {
                        'solution': 'Choose natural paint alternatives',
                        'effectiveness': 'Medium',
                        'implementation': 'Easy',
                        'cost': 'Medium',
                        'description': 'Use low-VOC or natural paint products'
                    },
                    {
                        'solution': 'Proper disposal of acrylic products',
                        'effectiveness': 'Medium',
                        'implementation': 'Easy',
                        'cost': 'Low',
                        'description': 'Ensure proper disposal of acrylic-containing products'
                    }
                ]
            },
            'remediation': {
                'filtration': [
                    {
                        'solution': 'Install microplastic filtration systems',
                        'effectiveness': 'High',
                        'implementation': 'Medium',
                        'cost': 'High',
                        'description': 'Install advanced filtration systems in water treatment facilities'
                    },
                    {
                        'solution': 'Use biofiltration methods',
                        'effectiveness': 'Medium',
                        'implementation': 'Medium',
                        'cost': 'Medium',
                        'description': 'Implement biological filtration systems using plants and microorganisms'
                    }
                ],
                'cleanup': [
                    {
                        'solution': 'Beach and waterway cleanup programs',
                        'effectiveness': 'Medium',
                        'implementation': 'Easy',
                        'cost': 'Low',
                        'description': 'Organize or participate in regular cleanup activities'
                    },
                    {
                        'solution': 'Automated cleanup systems',
                        'effectiveness': 'High',
                        'implementation': 'Hard',
                        'cost': 'Very High',
                        'description': 'Deploy automated systems for large-scale microplastic removal'
                    }
                ]
            },
            'monitoring': [
                {
                    'solution': 'Regular water quality testing',
                    'effectiveness': 'High',
                    'implementation': 'Medium',
                    'cost': 'Medium',
                    'description': 'Implement regular monitoring programs to track microplastic levels'
                },
                {
                    'solution': 'Citizen science programs',
                    'effectiveness': 'Medium',
                    'implementation': 'Easy',
                    'cost': 'Low',
                    'description': 'Engage community members in data collection and monitoring'
                }
            ]
        }
    
    def get_recommendations(self, analysis_result, comparison_data):
        """Generate personalized recommendations based on analysis results"""
        try:
            recommendations = {
                'timestamp': datetime.now().isoformat(),
                'priority_level': 'Medium',
                'prevention_solutions': [],
                'remediation_solutions': [],
                'monitoring_solutions': [],
                'implementation_plan': {},
                'cost_estimate': {},
                'timeline': {}
            }
            
            # Analyze detected microplastic types
            detected_types = analysis_result.get('types', [])
            particle_count = analysis_result.get('particle_count', 0)
            size_distribution = analysis_result.get('size_distribution', {})
            
            # Determine priority level
            recommendations['priority_level'] = self._determine_priority(analysis_result, comparison_data)
            
            # Get prevention solutions for detected types
            for microplastic_type in detected_types:
                if microplastic_type in self.solution_database['prevention']:
                    solutions = self.solution_database['prevention'][microplastic_type]
                    recommendations['prevention_solutions'].extend(solutions)
            
            # Get remediation solutions based on particle count and size
            if particle_count > 50:
                recommendations['remediation_solutions'].extend(self.solution_database['remediation']['filtration'])
            if particle_count > 100:
                recommendations['remediation_solutions'].extend(self.solution_database['remediation']['cleanup'])
            
            # Add monitoring solutions
            recommendations['monitoring_solutions'] = self.solution_database['monitoring']
            
            # Create implementation plan
            recommendations['implementation_plan'] = self._create_implementation_plan(recommendations)
            
            # Estimate costs
            recommendations['cost_estimate'] = self._estimate_costs(recommendations)
            
            # Create timeline
            recommendations['timeline'] = self._create_timeline(recommendations)
            
            # Remove duplicates and sort by effectiveness
            recommendations = self._optimize_recommendations(recommendations)
            
            return recommendations
            
        except Exception as e:
            print(f"Recommendation generation failed: {e}")
            return {'error': f'Failed to generate recommendations: {str(e)}'}
    
    def _determine_priority(self, analysis_result, comparison_data):
        """Determine priority level based on analysis results"""
        particle_count = analysis_result.get('particle_count', 0)
        risk_assessment = comparison_data.get('risk_assessment', {})
        
        if particle_count > 100 or risk_assessment.get('environmental_risk') == 'High':
            return 'Very High'
        elif particle_count > 50 or risk_assessment.get('environmental_risk') == 'Moderate':
            return 'High'
        elif particle_count > 20:
            return 'Medium'
        else:
            return 'Low'
    
    def _create_implementation_plan(self, recommendations):
        """Create a step-by-step implementation plan"""
        plan = {
            'phase_1': {
                'name': 'Immediate Actions (0-3 months)',
                'actions': []
            },
            'phase_2': {
                'name': 'Short-term Solutions (3-12 months)',
                'actions': []
            },
            'phase_3': {
                'name': 'Long-term Solutions (1-3 years)',
                'actions': []
            }
        }
        
        # Categorize solutions by implementation difficulty
        for solution in recommendations['prevention_solutions']:
            if solution['implementation'] == 'Easy':
                plan['phase_1']['actions'].append(solution)
            elif solution['implementation'] == 'Medium':
                plan['phase_2']['actions'].append(solution)
            else:
                plan['phase_3']['actions'].append(solution)
        
        for solution in recommendations['remediation_solutions']:
            if solution['implementation'] == 'Easy':
                plan['phase_1']['actions'].append(solution)
            elif solution['implementation'] == 'Medium':
                plan['phase_2']['actions'].append(solution)
            else:
                plan['phase_3']['actions'].append(solution)
        
        return plan
    
    def _estimate_costs(self, recommendations):
        """Estimate implementation costs"""
        cost_estimate = {
            'total_estimated_cost': 'Unknown',
            'cost_breakdown': {},
            'funding_sources': []
        }
        
        # Simple cost estimation based on solution complexity
        total_cost = 0
        cost_breakdown = {
            'prevention': 0,
            'remediation': 0,
            'monitoring': 0
        }
        
        for solution in recommendations['prevention_solutions']:
            if solution['cost'] == 'Low':
                cost_breakdown['prevention'] += 1000
            elif solution['cost'] == 'Medium':
                cost_breakdown['prevention'] += 5000
            elif solution['cost'] == 'High':
                cost_breakdown['prevention'] += 20000
        
        for solution in recommendations['remediation_solutions']:
            if solution['cost'] == 'Low':
                cost_breakdown['remediation'] += 2000
            elif solution['cost'] == 'Medium':
                cost_breakdown['remediation'] += 10000
            elif solution['cost'] == 'High':
                cost_breakdown['remediation'] += 50000
            elif solution['cost'] == 'Very High':
                cost_breakdown['remediation'] += 100000
        
        total_cost = sum(cost_breakdown.values())
        
        if total_cost < 10000:
            cost_estimate['total_estimated_cost'] = 'Low ($0-$10,000)'
        elif total_cost < 50000:
            cost_estimate['total_estimated_cost'] = 'Medium ($10,000-$50,000)'
        else:
            cost_estimate['total_estimated_cost'] = 'High ($50,000+)'
        
        cost_estimate['cost_breakdown'] = cost_breakdown
        cost_estimate['funding_sources'] = [
            'Government grants',
            'Environmental organizations',
            'Corporate sponsorships',
            'Community fundraising'
        ]
        
        return cost_estimate
    
    def _create_timeline(self, recommendations):
        """Create implementation timeline"""
        timeline = {
            'immediate': '0-3 months',
            'short_term': '3-12 months',
            'long_term': '1-3 years',
            'milestones': []
        }
        
        # Add milestones based on priority
        if recommendations['priority_level'] in ['Very High', 'High']:
            timeline['milestones'].append({
                'timeframe': '1 month',
                'milestone': 'Complete immediate prevention actions'
            })
            timeline['milestones'].append({
                'timeframe': '6 months',
                'milestone': 'Implement short-term solutions'
            })
            timeline['milestones'].append({
                'timeframe': '2 years',
                'milestone': 'Complete long-term infrastructure improvements'
            })
        
        return timeline
    
    def _optimize_recommendations(self, recommendations):
        """Remove duplicates and optimize recommendations"""
        # Remove duplicate solutions
        seen_solutions = set()
        optimized_solutions = []
        
        for solution in recommendations['prevention_solutions']:
            solution_key = solution['solution']
            if solution_key not in seen_solutions:
                seen_solutions.add(solution_key)
                optimized_solutions.append(solution)
        
        recommendations['prevention_solutions'] = optimized_solutions
        
        # Sort by effectiveness
        effectiveness_order = {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        recommendations['prevention_solutions'].sort(
            key=lambda x: effectiveness_order.get(x['effectiveness'], 0), 
            reverse=True
        )
        
        return recommendations
