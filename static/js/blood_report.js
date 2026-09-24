class BloodReportAnalyzer {
    constructor() {
        this.currentFile = null;
        this.analysisData = null;
        this.pdfFilename = null;
        
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.filePreview = document.getElementById('filePreview');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeFileBtn = document.getElementById('removeFile');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.patientDetails = document.getElementById('patientDetails');
        this.parametersTable = document.getElementById('parametersTable');
        this.summaryList = document.getElementById('summaryList');
        this.disclaimerText = document.getElementById('disclaimerText');
        
        // Modal elements
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.closeModal = document.getElementById('closeModal');
        this.closeError = document.getElementById('closeError');
    }
    
    bindEvents() {
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // File input change
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Control buttons
        this.removeFileBtn.addEventListener('click', () => this.removeFile());
        this.analyzeBtn.addEventListener('click', () => this.analyzeReport());
        this.downloadBtn.addEventListener('click', () => this.downloadPDF());
        
        // Modal events
        this.closeModal.addEventListener('click', () => this.hideErrorModal());
        this.closeError.addEventListener('click', () => this.hideErrorModal());
        
        // Click outside modal to close
        this.errorModal.addEventListener('click', (e) => {
            if (e.target === this.errorModal) {
                this.hideErrorModal();
            }
        });
    }
    
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }
    
    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }
    
    processFile(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
        if (!validTypes.includes(file.type)) {
            this.showError('Please select a valid image file (JPG, PNG) or PDF.');
            return;
        }
        
        // Validate file size (max 16MB)
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (file.size > maxSize) {
            this.showError('File size must be less than 16MB.');
            return;
        }
        
        this.currentFile = file;
        this.showFilePreview();
    }
    
    showFilePreview() {
        if (!this.currentFile) return;
        
        this.fileName.textContent = this.currentFile.name;
        this.fileSize.textContent = this.formatFileSize(this.currentFile.size);
        
        this.uploadArea.style.display = 'none';
        this.filePreview.style.display = 'block';
    }
    
    removeFile() {
        this.currentFile = null;
        this.fileInput.value = '';
        
        this.uploadArea.style.display = 'block';
        this.filePreview.style.display = 'none';
        this.resultsSection.style.display = 'none';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    async analyzeReport() {
        if (!this.currentFile) {
            this.showError('Please select a file first.');
            return;
        }
        
        this.showLoading();
        this.analyzeBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('file', this.currentFile);
        
        try {
            const response = await fetch('/process-blood', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.analysisData = data.analysis_data;
                this.pdfFilename = data.pdf_filename;
                this.displayResults();
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || 'Failed to analyze the report. Please try again.');
        } finally {
            this.hideLoading();
            this.analyzeBtn.disabled = false;
        }
    }
    
    displayResults() {
        if (!this.analysisData) return;
        
        const data = typeof this.analysisData === 'string' 
            ? JSON.parse(this.analysisData) 
            : this.analysisData;
        
        // Show results section
        this.resultsSection.style.display = 'block';
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Display patient details
        this.displayPatientDetails(data.patient_details);
        
        // Display blood parameters
        this.displayBloodParameters(data.blood_parameters);
        
        // Display summary
        this.displaySummary(data.summary);
        
        // Display disclaimer
        this.displayDisclaimer(data.disclaimer);
    }
    
    displayPatientDetails(patientDetails) {
        if (!patientDetails) {
            this.patientDetails.innerHTML = '<p>No patient details available</p>';
            return;
        }
        
        const fields = [
            { label: 'Name', value: patientDetails.name },
            { label: 'Age', value: patientDetails.age },
            { label: 'Gender', value: patientDetails.gender },
            { label: 'Patient ID', value: patientDetails.id }
        ].filter(field => field.value && field.value !== 'N/A');
        
        if (fields.length === 0) {
            this.patientDetails.innerHTML = '<p>No patient details available</p>';
            return;
        }
        
        const html = `
            <div class="patient-info">
                ${fields.map(field => `
                    <div class="patient-field">
                        <div class="field-label">${field.label}</div>
                        <div class="field-value">${field.value}</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        this.patientDetails.innerHTML = html;
    }
    
    displayBloodParameters(parameters) {
        if (!parameters || parameters.length === 0) {
            this.parametersTable.innerHTML = '<p>No blood parameters available</p>';
            return;
        }
        
        const tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                        <th>Reference Range</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${parameters.map(param => `
                        <tr>
                            <td>${param.parameter || 'N/A'}</td>
                            <td>${param.value || 'N/A'}</td>
                            <td>${param.reference_range || 'N/A'}</td>
                            <td class="status-${param.status?.toLowerCase() || 'normal'}">
                                ${param.status ? param.status.toUpperCase() : 'N/A'}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        this.parametersTable.innerHTML = tableHTML;
    }
    
    displaySummary(summary) {
        if (!summary || summary.length === 0) {
            this.summaryList.innerHTML = '<p>No summary available</p>';
            return;
        }
        
        const html = summary.map(item => `
            <div class="summary-item">${item}</div>
        `).join('');
        
        this.summaryList.innerHTML = html;
    }
    
    displayDisclaimer(disclaimer) {
        if (!disclaimer) {
            this.disclaimerText.innerHTML = `
                <p><strong>This analysis is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment.</strong></p>
                <p>Always consult with a qualified healthcare provider regarding any health concerns or before making any decisions related to your health or treatment.</p>
                <p>The AI analysis may not capture all nuances of your medical condition and should be reviewed by a medical professional.</p>
            `;
            return;
        }
        
        if (Array.isArray(disclaimer)) {
            const html = disclaimer.map(item => `<p>${item}</p>`).join('');
            this.disclaimerText.innerHTML = html;
        } else {
            this.disclaimerText.innerHTML = `<p>${disclaimer}</p>`;
        }
    }
    
    async downloadPDF() {
    if (!this.pdfFilename) {
        this.showError('No PDF available for download.');
        return;
    }

    try {
        const response = await fetch(
            `/download/${encodeURIComponent(this.pdfFilename)}`
        );

        if (response.ok) {
            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'blood_report_analysis.pdf';

            document.body.appendChild(a);
            a.click();

            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('Failed to download PDF.');
        }

    } catch (error) {
        console.error('Download error:', error);
        this.showError(
            error.message || 'Failed to download PDF. Please try again.'
        );
    }
}
    
    showLoading() {
        this.loadingOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    hideLoading() {
        this.loadingOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    hideErrorModal() {
        this.errorModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Initialize the analyzer when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BloodReportAnalyzer();
});