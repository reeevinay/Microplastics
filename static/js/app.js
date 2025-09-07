// Microplastic Analysis System - Frontend JavaScript

class MicroplasticAnalyzer {
    constructor() {
        this.initializeEventListeners();
        this.loadHistory();
    }

    initializeEventListeners() {
        // File input change
        document.getElementById('imageInput').addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // Drag and drop
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // Click to upload
        uploadArea.addEventListener('click', () => {
            document.getElementById('imageInput').click();
        });

        // Analyze button
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzeImage();
        });

        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearUpload();
        });
    }

    handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showAlert('Please select a valid image file.', 'danger');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showAlert('File size must be less than 10MB.', 'danger');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewImg = document.getElementById('previewImg');
            previewImg.src = e.target.result;
            document.getElementById('imagePreview').classList.remove('d-none');
            document.getElementById('uploadArea').style.display = 'none';
        };
        reader.readAsDataURL(file);

        this.selectedFile = file;
    }

    async analyzeImage() {
        if (!this.selectedFile) {
            this.showAlert('Please select an image first.', 'warning');
            return;
        }

        // Show loading
        this.showLoading(true);
        document.getElementById('results').classList.add('d-none');

        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
                this.loadHistory(); // Refresh history
            } else {
                this.showAlert(result.error || 'Analysis failed.', 'danger');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showAlert('Network error. Please try again.', 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        const { analysis, comparison, recommendations } = result;

        // Update summary cards
        document.getElementById('particleCount').textContent = analysis.particle_count || 0;
        document.getElementById('typesFound').textContent = analysis.types ? analysis.types.length : 0;
        
        const riskLevel = comparison.risk_assessment?.environmental_risk || 'Unknown';
        document.getElementById('riskLevel').textContent = riskLevel;
        document.getElementById('riskLevel').className = `text-${this.getRiskColor(riskLevel)}`;

        const avgConfidence = analysis.average_confidence || 0;
        document.getElementById('confidence').textContent = `${Math.round(avgConfidence * 100)}%`;

        // Create type distribution chart
        this.createTypeChart(analysis);

        // Create size distribution chart
        this.createSizeChart(analysis);

        // Display detailed results
        this.displayDetailedResults(analysis, comparison);

        // Display recommendations
        this.displayRecommendations(recommendations);

        // Show results section
        document.getElementById('results').classList.remove('d-none');
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }

    createTypeChart(analysis) {
        const types = analysis.types || [];
        const counts = analysis.counts || [];

        if (types.length === 0) {
            document.getElementById('typeChart').innerHTML = '<p class="text-muted text-center">No microplastics detected</p>';
            return;
        }

        // Truncate long type names for better display based on screen size
        const screenWidth = window.innerWidth;
        let maxLength = 20;
        
        if (screenWidth < 576) {
            maxLength = 8;  // Very small screens
        } else if (screenWidth < 768) {
            maxLength = 12; // Small screens
        } else if (screenWidth < 1200) {
            maxLength = 16; // Medium screens
        }
        
        const truncatedTypes = types.map(type => {
            if (type.length > maxLength) {
                return type.substring(0, maxLength - 3) + '...';
            }
            return type;
        });

        const data = [{
            values: counts,
            labels: truncatedTypes,
            type: 'pie',
            textinfo: 'label+percent',
            textposition: 'outside',
            marker: {
                colors: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22'],
                line: {
                    color: '#ffffff',
                    width: 2
                }
            },
            hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        }];

        // Responsive layout based on screen size
        const isMobile = screenWidth < 768;
        const isSmallMobile = screenWidth < 576;
        
        const layout = {
            title: {
                text: 'Microplastic Types Distribution',
                font: { size: isSmallMobile ? 12 : isMobile ? 13 : 14 }
            },
            font: { size: isSmallMobile ? 9 : isMobile ? 10 : 11 },
            margin: { 
                t: isSmallMobile ? 50 : isMobile ? 55 : 60, 
                b: isSmallMobile ? 30 : isMobile ? 35 : 40, 
                l: isSmallMobile ? 30 : isMobile ? 35 : 40, 
                r: isSmallMobile ? 30 : isMobile ? 35 : 40 
            },
            legend: {
                orientation: isMobile ? 'h' : 'v',
                x: isMobile ? 0.5 : 1.05,
                y: isMobile ? -0.1 : 0.5,
                xanchor: isMobile ? 'center' : 'left',
                yanchor: isMobile ? 'top' : 'middle',
                font: { size: isSmallMobile ? 8 : isMobile ? 9 : 10 }
            },
            showlegend: true
        };

        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };

        Plotly.newPlot('typeChart', data, layout, config);
    }

    createSizeChart(analysis) {
        const sizeDist = analysis.size_distribution || {};
        const categories = Object.keys(sizeDist);
        const values = Object.values(sizeDist);

        if (categories.length === 0) {
            document.getElementById('sizeChart').innerHTML = '<p class="text-muted text-center">No size data available</p>';
            return;
        }

        const data = [{
            x: categories,
            y: values,
            type: 'bar',
            marker: {
                color: ['#e74c3c', '#f39c12', '#2ecc71'],
                line: {
                    color: '#ffffff',
                    width: 1
                }
            },
            hovertemplate: '<b>%{x}</b><br>Particles: %{y}<extra></extra>'
        }];

        // Responsive layout for size chart
        const screenWidth = window.innerWidth;
        const isMobile = screenWidth < 768;
        const isSmallMobile = screenWidth < 576;
        
        const layout = {
            title: {
                text: 'Particle Size Distribution',
                font: { size: isSmallMobile ? 12 : isMobile ? 13 : 14 }
            },
            xaxis: { 
                title: 'Size Category',
                titlefont: { size: isSmallMobile ? 10 : isMobile ? 11 : 12 },
                tickfont: { size: isSmallMobile ? 9 : isMobile ? 10 : 11 }
            },
            yaxis: { 
                title: 'Number of Particles',
                titlefont: { size: isSmallMobile ? 10 : isMobile ? 11 : 12 },
                tickfont: { size: isSmallMobile ? 9 : isMobile ? 10 : 11 }
            },
            font: { size: isSmallMobile ? 9 : isMobile ? 10 : 11 },
            margin: { 
                t: isSmallMobile ? 50 : isMobile ? 55 : 60, 
                b: isSmallMobile ? 50 : isMobile ? 55 : 60, 
                l: isSmallMobile ? 50 : isMobile ? 55 : 60, 
                r: isSmallMobile ? 30 : isMobile ? 35 : 40 
            }
        };

        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };

        Plotly.newPlot('sizeChart', data, layout, config);
    }

    displayDetailedResults(analysis, comparison) {
        const container = document.getElementById('detailedResults');
        
        let html = '<div class="row">';
        
        // Analysis details
        html += '<div class="col-md-6">';
        html += '<h6 class="text-primary mb-3"><i class="fas fa-info-circle me-2"></i>Analysis Details</h6>';
        html += '<ul class="list-group list-group-flush">';
        
        if (analysis.types && analysis.types.length > 0) {
            analysis.types.forEach((type, index) => {
                const count = analysis.counts[index] || 0;
                const confidence = analysis.confidence_scores[index] || 0;
                html += `<li class="list-group-item d-flex justify-content-between align-items-center">
                    ${type}
                    <span class="badge bg-primary rounded-pill">${count} particles</span>
                </li>`;
            });
        } else {
            html += '<li class="list-group-item text-muted">No microplastics detected</li>';
        }
        
        html += '</ul></div>';
        
        // Comparison data
        html += '<div class="col-md-6">';
        html += '<h6 class="text-success mb-3"><i class="fas fa-chart-line me-2"></i>Comparison with Baseline</h6>';
        
        if (comparison.baseline_comparison) {
            html += '<ul class="list-group list-group-flush">';
            Object.entries(comparison.baseline_comparison).forEach(([type, data]) => {
                const status = data.concentration_status || 'Unknown';
                const statusColor = this.getStatusColor(status);
                html += `<li class="list-group-item">
                    <strong>${type}</strong><br>
                    <small class="text-muted">Sample: ${data.sample_percentage}% | 
                    <span class="badge bg-${statusColor}">${status}</span></small>
                </li>`;
            });
            html += '</ul>';
        } else {
            html += '<p class="text-muted">No comparison data available</p>';
        }
        
        html += '</div></div>';
        
        container.innerHTML = html;
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendations');
        
        if (!recommendations || !recommendations.prevention_solutions) {
            container.innerHTML = '<p class="text-muted">No recommendations available</p>';
            return;
        }

        let html = `<div class="alert alert-info">
            <h6><i class="fas fa-info-circle me-2"></i>Priority Level: 
            <span class="badge bg-${this.getPriorityColor(recommendations.priority_level)}">
                ${recommendations.priority_level}
            </span></h6>
        </div>`;

        // Prevention solutions
        if (recommendations.prevention_solutions.length > 0) {
            html += '<h6 class="text-success mb-3"><i class="fas fa-shield-alt me-2"></i>Prevention Solutions</h6>';
            recommendations.prevention_solutions.slice(0, 5).forEach(solution => {
                html += `<div class="recommendation-item">
                    <h6>${solution.solution}</h6>
                    <p class="mb-2">${solution.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="effectiveness-badge effectiveness-${solution.effectiveness.toLowerCase()}">
                            ${solution.effectiveness} Effectiveness
                        </span>
                        <small class="text-muted">Cost: ${solution.cost} | Implementation: ${solution.implementation}</small>
                    </div>
                </div>`;
            });
        }

        // Implementation plan
        if (recommendations.implementation_plan) {
            html += '<h6 class="text-primary mb-3 mt-4"><i class="fas fa-calendar-alt me-2"></i>Implementation Plan</h6>';
            Object.entries(recommendations.implementation_plan).forEach(([phase, data]) => {
                if (data.actions && data.actions.length > 0) {
                    html += `<div class="card mb-3">
                        <div class="card-header">
                            <h6 class="mb-0">${data.name}</h6>
                        </div>
                        <div class="card-body">
                            <ul class="mb-0">`;
                    data.actions.slice(0, 3).forEach(action => {
                        html += `<li>${action.solution}</li>`;
                    });
                    html += '</ul></div></div>';
                }
            });
        }

        container.innerHTML = html;
    }

    async loadHistory() {
        try {
            const response = await fetch('/history');
            const history = await response.json();
            this.displayHistory(history);
        } catch (error) {
            console.error('Error loading history:', error);
            document.getElementById('historyContent').innerHTML = 
                '<p class="text-muted text-center">Error loading history</p>';
        }
    }

    displayHistory(history) {
        const container = document.getElementById('historyContent');
        
        if (history.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No analysis history found</p>';
            return;
        }

        let html = '';
        history.forEach((item, index) => {
            const date = new Date(item.date).toLocaleDateString();
            const time = new Date(item.date).toLocaleTimeString();
            const types = item.microplastic_types || [];
            
            html += `<div class="history-item" data-analysis-id="${item.id}">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                        <div class="filename">${item.filename}</div>
                        <div class="date">${date} at ${time}</div>
                        <div class="mt-2">
                            <small class="text-muted">Types found: ${types.join(', ') || 'None'}</small>
                        </div>
                    </div>
                    <div class="text-end">
                        <span class="badge bg-primary">${item.particle_count} particles</span><br>
                        <small class="text-muted">${types.length} types</small><br>
                        <button class="btn btn-sm btn-outline-primary mt-1" onclick="viewHistoryDetails(${item.id})">
                            <i class="fas fa-eye"></i> View Details
                        </button>
                    </div>
                </div>
            </div>`;
        });

        container.innerHTML = html;
    }

    clearUpload() {
        document.getElementById('imageInput').value = '';
        document.getElementById('imagePreview').classList.add('d-none');
        document.getElementById('uploadArea').style.display = 'block';
        document.getElementById('results').classList.add('d-none');
        this.selectedFile = null;
    }

    showLoading(show) {
        const loadingSection = document.getElementById('loading');
        if (show) {
            loadingSection.classList.remove('d-none');
        } else {
            loadingSection.classList.add('d-none');
        }
    }

    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at the top of the upload section
        const uploadSection = document.getElementById('upload');
        uploadSection.insertBefore(alertDiv, uploadSection.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    getRiskColor(risk) {
        switch (risk.toLowerCase()) {
            case 'low': return 'success';
            case 'medium': return 'warning';
            case 'high': return 'danger';
            default: return 'secondary';
        }
    }

    getStatusColor(status) {
        switch (status.toLowerCase()) {
            case 'normal': return 'success';
            case 'elevated': return 'warning';
            case 'below average': return 'info';
            default: return 'secondary';
        }
    }

    getPriorityColor(priority) {
        switch (priority.toLowerCase()) {
            case 'very high': return 'danger';
            case 'high': return 'warning';
            case 'medium': return 'info';
            case 'low': return 'success';
            default: return 'secondary';
        }
    }
}

// Utility functions
function scrollToUpload() {
    document.getElementById('upload').scrollIntoView({ behavior: 'smooth' });
}

// Global function for viewing history details
async function viewHistoryDetails(analysisId) {
    try {
        // This would typically fetch detailed data from the server
        // For now, we'll show a modal with basic info
        const historyItems = document.querySelectorAll('.history-item');
        const targetItem = Array.from(historyItems).find(item => 
            item.getAttribute('data-analysis-id') == analysisId
        );
        
        if (targetItem) {
            const filename = targetItem.querySelector('.filename').textContent;
            const date = targetItem.querySelector('.date').textContent;
            const particleCount = targetItem.querySelector('.badge').textContent;
            
            // Create and show modal
            const modalHtml = `
                <div class="modal fade" id="historyModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Analysis Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h6>File: ${filename}</h6>
                                <p><strong>Date:</strong> ${date}</p>
                                <p><strong>Particles Found:</strong> ${particleCount}</p>
                                <div class="alert alert-info">
                                    <i class="fas fa-info-circle"></i>
                                    Detailed analysis data would be displayed here. 
                                    This feature can be expanded to show full analysis results, 
                                    charts, and recommendations from the selected analysis.
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remove existing modal if any
            const existingModal = document.getElementById('historyModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Add modal to body
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('historyModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error viewing history details:', error);
        alert('Error loading analysis details');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MicroplasticAnalyzer();
    
    // Add window resize listener for responsive charts
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // Re-render charts if they exist
            const typeChart = document.getElementById('typeChart');
            const sizeChart = document.getElementById('sizeChart');
            
            if (typeChart && typeChart.data) {
                Plotly.redraw('typeChart');
            }
            if (sizeChart && sizeChart.data) {
                Plotly.redraw('sizeChart');
            }
        }, 250);
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
