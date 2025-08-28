#!/usr/bin/env python3
"""
Loan Prediction Web Application
Flask API Backend for serving ML model predictions
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import logging
import os
from src.loan_predictor.loan_predictor import LoanPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load the trained model
try:
    predictor = LoanPredictor()
    predictor.load_model('loan_predictor_model.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    predictor = None

@app.route('/')
def home():
    """Serve the main web application page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint for loan predictions
    
    Expected JSON format:
    {
        "gender": "Male/Female",
        "married": "Yes/No", 
        "dependents": "0/1/2/3+",
        "education": "Graduate/Not Graduate",
        "self_employed": "Yes/No",
        "applicant_income": float,
        "coapplicant_income": float,
        "loan_amount": float,
        "loan_amount_term": float,
        "credit_history": "1.0/0.0",
        "property_area": "Urban/Semiurban/Rural"
    }
    """
    try:
        if not predictor:
            return jsonify({
                'error': 'Model not loaded',
                'success': False
            }), 500

        # Get data from request
        data = request.json
        logger.info(f"Received prediction request: {data}")

        # Validate required fields
        required_fields = [
            'gender', 'married', 'dependents', 'education', 'self_employed',
            'applicant_income', 'coapplicant_income', 'loan_amount', 
            'loan_amount_term', 'credit_history', 'property_area'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}',
                'success': False
            }), 400

        # Create applicant data dictionary
        # Convert annual income to monthly for model compatibility
        # Convert loan amount from full dollars to thousands for model
        applicant_data = {
            'Gender': data['gender'],
            'Married': data['married'],
            'Dependents': data['dependents'],
            'Education': data['education'],
            'Self_Employed': data['self_employed'],
            'ApplicantIncome': float(data['applicant_income']) / 12,  # Convert annual to monthly
            'CoapplicantIncome': float(data['coapplicant_income']) / 12,  # Convert annual to monthly
            'LoanAmount': float(data['loan_amount']) / 1000,  # Convert to thousands for model
            'Loan_Amount_Term': float(data['loan_amount_term']),
            'Credit_History': float(data['credit_history']),
            'Property_Area': data['property_area']
        }

        # Make prediction using the existing method
        result = predictor.predict_loan(applicant_data)
        prediction = 'Y' if result['approved'] else 'N'
        probability = result['probability']

        # Format response with original user input values for display
        display_data = {
            'Gender': data['gender'],
            'Married': data['married'],
            'Dependents': data['dependents'],
            'Education': data['education'],
            'Self_Employed': data['self_employed'],
            'ApplicantIncome': float(data['applicant_income']),  # Keep original annual income
            'CoapplicantIncome': float(data['coapplicant_income']),  # Keep original annual income
            'LoanAmount': float(data['loan_amount']),  # Keep original full dollar amount
            'Loan_Amount_Term': float(data['loan_amount_term']),
            'Credit_History': float(data['credit_history']),
            'Property_Area': data['property_area']
        }
        
        response = {
            'success': True,
            'prediction': prediction,
            'probability': round(probability * 100, 2),
            'status': 'approved' if prediction == 'Y' else 'rejected',
            'confidence': 'high' if probability > 0.7 or probability < 0.3 else 'moderate',
            'applicant_data': display_data
        }

        logger.info(f"Prediction result: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Get port from environment variable (Railway uses this) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=port)