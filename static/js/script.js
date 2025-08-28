// Loan Prediction System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Loan Prediction System Initialized');
    
    // Initialize form
    initializeForm();
    
    // Add smooth scrolling
    initializeSmoothScrolling();
    
    // Add navbar scroll effects
    initializeNavbarEffects();
});

function initializeForm() {
    const form = document.getElementById('loanForm');
    const submitBtn = document.getElementById('submitBtn');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        setLoadingState(true);
        
        try {
            // Collect form data
            const formData = collectFormData();
            
            // Validate form data
            if (!validateFormData(formData)) {
                setLoadingState(false);
                return;
            }
            
            // Make API call
            const result = await makePredictionAPI(formData);
            
            // Display results
            displayResults(result);
            
        } catch (error) {
            console.error('Prediction error:', error);
            showError('Unable to process prediction. Please try again.');
        } finally {
            setLoadingState(false);
        }
    });
}

function collectFormData() {
    const form = document.getElementById('loanForm');
    const formData = new FormData(form);
    
    const data = {
        gender: formData.get('gender'),
        married: formData.get('married'),
        dependents: formData.get('dependents'),
        education: formData.get('education'),
        self_employed: formData.get('self_employed'),
        applicant_income: parseFloat(formData.get('applicant_income')),
        coapplicant_income: parseFloat(formData.get('coapplicant_income')) || 0,
        loan_amount: parseFloat(formData.get('loan_amount')),
        loan_amount_term: parseFloat(formData.get('loan_amount_term')),
        credit_history: formData.get('credit_history'),
        property_area: formData.get('property_area')
    };
    
    console.log('Form data collected:', data);
    return data;
}

function validateFormData(data) {
    const requiredFields = [
        'gender', 'married', 'dependents', 'education', 'self_employed',
        'applicant_income', 'loan_amount', 'loan_amount_term', 
        'credit_history', 'property_area'
    ];
    
    for (let field of requiredFields) {
        if (!data[field] && data[field] !== 0) {
            showError(`Please fill in the ${field.replace('_', ' ')} field`);
            return false;
        }
    }
    
    // Additional validation
    if (data.applicant_income <= 0) {
        showError('Applicant income must be greater than 0');
        return false;
    }
    
    if (data.loan_amount <= 0) {
        showError('Loan amount must be greater than 0');
        return false;
    }
    
    return true;
}

async function makePredictionAPI(data) {
    console.log('Making API call with data:', data);
    
    const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API request failed');
    }
    
    const result = await response.json();
    console.log('API response:', result);
    return result;
}

function displayResults(result) {
    // Hide form section and show results
    document.getElementById('application').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    
    // Update result status
    const statusElement = document.getElementById('resultStatus');
    statusElement.textContent = result.status.toUpperCase();
    statusElement.className = `result-status ${result.status}`;
    
    // Update prediction result text
    const predictionElement = document.getElementById('predictionResult');
    if (result.prediction === 'Y') {
        predictionElement.innerHTML = `
            <div style="color: var(--secondary-color);">
                <i class="fas fa-check-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <div>Congratulations! Your loan application is likely to be <strong>APPROVED</strong></div>
            </div>
        `;
    } else {
        predictionElement.innerHTML = `
            <div style="color: var(--danger-color);">
                <i class="fas fa-times-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <div>Unfortunately, your loan application may be <strong>REJECTED</strong></div>
            </div>
        `;
    }
    
    // Update probability circle
    updateProbabilityCircle(result.probability);
    
    // Update result details
    updateResultDetails(result);
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

function updateProbabilityCircle(probability) {
    const circle = document.getElementById('progressCircle');
    const probabilityValue = document.getElementById('probabilityValue');
    
    // Calculate circle progress
    const circumference = 2 * Math.PI * 54; // radius = 54
    const offset = circumference - (probability / 100) * circumference;
    
    // Animate the circle
    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
        
        // Update probability text with animation
        animateNumber(0, probability, 1000, (value) => {
            probabilityValue.textContent = Math.round(value) + '%';
        });
    }, 100);
    
    // Update circle color based on probability
    if (probability >= 70) {
        circle.style.stroke = 'var(--secondary-color)';
    } else if (probability >= 40) {
        circle.style.stroke = 'var(--warning-color)';
    } else {
        circle.style.stroke = 'var(--danger-color)';
    }
}

function updateResultDetails(result) {
    const detailsElement = document.getElementById('resultDetails');
    
    const totalIncome = result.applicant_data.ApplicantIncome + result.applicant_data.CoapplicantIncome;
    const loanAmount = result.applicant_data.LoanAmount; // Already in full dollars
    const monthlyPayment = calculateMonthlyPayment(loanAmount, result.applicant_data.Loan_Amount_Term);
    const loanToIncomeRatio = ((monthlyPayment * 12) / totalIncome * 100).toFixed(1);
    
    detailsElement.innerHTML = `
        <h4 style="margin-bottom: 1rem; color: var(--gray-900);">Assessment Details</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="detail-item">
                <strong>Total Income:</strong><br>
                $${totalIncome.toLocaleString()}/year
            </div>
            <div class="detail-item">
                <strong>Loan Amount:</strong><br>
                $${loanAmount.toLocaleString()}
            </div>
            <div class="detail-item">
                <strong>Monthly Payment:</strong><br>
                $${monthlyPayment.toLocaleString()}
            </div>
            <div class="detail-item">
                <strong>Loan-to-Income:</strong><br>
                ${loanToIncomeRatio}%
            </div>
            <div class="detail-item">
                <strong>Credit History:</strong><br>
                ${result.applicant_data.Credit_History === 1 ? 'Good' : 'Poor'}
            </div>
            <div class="detail-item">
                <strong>Confidence Level:</strong><br>
                ${result.confidence.charAt(0).toUpperCase() + result.confidence.slice(1)}
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: ${result.prediction === 'Y' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'}; border-radius: 8px; border-left: 4px solid ${result.prediction === 'Y' ? 'var(--secondary-color)' : 'var(--danger-color)'};">
            <h5 style="margin-bottom: 0.5rem; color: var(--gray-900);">
                ${result.prediction === 'Y' ? 'Why this application looks good:' : 'Areas of concern:'}
            </h5>
            <ul style="margin-left: 1rem; color: var(--gray-700);">
                ${generateInsights(result).map(insight => `<li>${insight}</li>`).join('')}
            </ul>
        </div>
    `;
}

function generateInsights(result) {
    const insights = [];
    const data = result.applicant_data;
    const totalIncome = data.ApplicantIncome + data.CoapplicantIncome;
    const loanAmount = data.LoanAmount * 1000;
    const monthlyPayment = calculateMonthlyPayment(loanAmount, data.Loan_Amount_Term);
    const loanToIncomeRatio = (monthlyPayment * 12) / totalIncome;
    
    if (result.prediction === 'Y') {
        if (data.Credit_History === 1) insights.push('Good credit history');
        if (data.Education === 'Graduate') insights.push('Graduate education level');
        if (loanToIncomeRatio < 0.4) insights.push('Healthy loan-to-income ratio');
        if (totalIncome > 50000) insights.push('Strong income level');
        if (data.CoapplicantIncome > 0) insights.push('Additional co-applicant income');
    } else {
        if (data.Credit_History === 0) insights.push('Poor credit history');
        if (loanToIncomeRatio > 0.5) insights.push('High loan-to-income ratio');
        if (totalIncome < 30000) insights.push('Low income level');
        if (data.Self_Employed === 'Yes') insights.push('Self-employment income uncertainty');
    }
    
    return insights.length ? insights : ['Multiple factors considered in this assessment'];
}

function calculateMonthlyPayment(loanAmount, termMonths, interestRate = 0.08) {
    const monthlyRate = interestRate / 12;
    const monthlyPayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, termMonths)) / 
                          (Math.pow(1 + monthlyRate, termMonths) - 1);
    return Math.round(monthlyPayment);
}

function animateNumber(start, end, duration, callback) {
    const startTime = Date.now();
    
    function update() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = start + (end - start) * easeOutCubic(progress);
        
        callback(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    update();
}

function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

function setLoadingState(loading) {
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('span');
    const loader = submitBtn.querySelector('.loader');
    
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        btnText.style.display = 'none';
        loader.style.display = 'block';
    } else {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
        btnText.style.display = 'inline';
        loader.style.display = 'none';
    }
}

function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--danger-color);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    errorDiv.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

function resetForm() {
    // Hide results and show form
    document.getElementById('results').style.display = 'none';
    document.getElementById('application').style.display = 'block';
    
    // Reset form
    document.getElementById('loanForm').reset();
    
    // Scroll to form
    document.getElementById('application').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

function downloadReport() {
    // Get result data
    const resultStatus = document.getElementById('resultStatus').textContent;
    const probabilityValue = document.getElementById('probabilityValue').textContent;
    
    // Create downloadable report content
    const reportContent = `
Loan Prediction Assessment Report
Generated on: ${new Date().toLocaleDateString()}
================================

Result: ${resultStatus}
Confidence Level: ${probabilityValue}

This report was generated by the AI-powered Loan Prediction System.
For official loan applications, please consult with your financial institution.
    `;
    
    // Create and download file
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `loan-prediction-report-${new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function initializeSmoothScrolling() {
    // Add smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'var(--white)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .detail-item {
        padding: 0.75rem;
        background: var(--white);
        border-radius: 6px;
        border: 1px solid var(--gray-200);
        text-align: center;
    }
`;
document.head.appendChild(style);