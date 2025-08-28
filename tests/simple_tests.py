#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from loan_predictor.loan_predictor import LoanPredictor
import pandas as pd
import numpy as np

def test_basic_functionality():
    """Simple test to verify the system works"""
    print("🧪 TESTING LOAN PREDICTION SYSTEM")
    print("=" * 40)
    
    predictor = LoanPredictor()
    
    # Test 1: Data Generation
    print("📊 Test 1: Data Generation")
    data = predictor.create_sample_data(100)
    print(f"✅ Generated {len(data)} records with {len(data.columns)} columns")
    
    # Test 2: Model Training
    print("\n🤖 Test 2: Model Training")
    results = predictor.train_models(data)
    best_accuracy = max(results.values())
    print(f"✅ Best model accuracy: {best_accuracy:.2%}")
    
    # Test 3: Prediction
    print("\n🎯 Test 3: Making Predictions")
    test_cases = [
        {
            'name': 'Good Applicant',
            'data': {
                'Gender': 'Male', 'Married': 'Yes', 'Dependents': 1,
                'Education': 'Graduate', 'Self_Employed': 'No',
                'ApplicantIncome': 6000, 'CoapplicantIncome': 2000,
                'LoanAmount': 120, 'Loan_Amount_Term': 360,
                'Credit_History': 1, 'Property_Area': 'Urban'
            }
        },
        {
            'name': 'Risky Applicant',
            'data': {
                'Gender': 'Female', 'Married': 'No', 'Dependents': 3,
                'Education': 'Not Graduate', 'Self_Employed': 'Yes',
                'ApplicantIncome': 2000, 'CoapplicantIncome': 0,
                'LoanAmount': 200, 'Loan_Amount_Term': 240,
                'Credit_History': 0, 'Property_Area': 'Rural'
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            result = predictor.predict_loan(test_case['data'])
            status = "APPROVED" if result['approved'] else "REJECTED"
            print(f"✅ {test_case['name']}: {status} ({result['probability']:.1%})")
        except Exception as e:
            print(f"❌ {test_case['name']}: Error - {e}")
    
    # Test 4: Model Persistence
    print("\n💾 Test 4: Model Save/Load")
    try:
        predictor.save_model('test_model.pkl')
        
        new_predictor = LoanPredictor()
        new_predictor.load_model('test_model.pkl')
        
        # Test prediction with loaded model
        result = new_predictor.predict_loan(test_cases[0]['data'])
        print(f"✅ Loaded model prediction: {result['probability']:.1%}")
        
    except Exception as e:
        print(f"❌ Model persistence error: {e}")
    
    print("\n🎉 ALL TESTS COMPLETED!")
    return True

def performance_test():
    """Test model performance with different data sizes"""
    print("\n📈 PERFORMANCE TESTING")
    print("=" * 30)
    
    predictor = LoanPredictor()
    data_sizes = [100, 500, 1000]
    
    for size in data_sizes:
        print(f"\n📊 Testing with {size} records...")
        data = predictor.create_sample_data(size)
        results = predictor.train_models(data)
        
        best_model = max(results.items(), key=lambda x: x[1])
        print(f"Best: {best_model[0]} ({best_model[1]:.2%})")
        
        # Quick predictions
        sample_applicant = {
            'Gender': 'Male', 'Married': 'Yes', 'Dependents': 1,
            'Education': 'Graduate', 'Self_Employed': 'No',
            'ApplicantIncome': 5000, 'CoapplicantIncome': 1500,
            'LoanAmount': 150, 'Loan_Amount_Term': 360,
            'Credit_History': 1, 'Property_Area': 'Urban'
        }
        
        result = predictor.predict_loan(sample_applicant)
        print(f"Sample prediction: {result['probability']:.1%}")

if __name__ == "__main__":
    # Run basic tests
    test_basic_functionality()
    
    # Run performance tests
    performance_test()