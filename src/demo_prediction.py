#!/usr/bin/env python3

import os
from loan_predictor.loan_predictor import LoanPredictor

def demo_predictions():
    """Demo the loan prediction system with sample applicants"""
    
    # Load the trained model
    predictor = LoanPredictor()
    model_path = os.path.join(os.path.dirname(__file__), '../models/loan_predictor_model.pkl')
    predictor.load_model(model_path)
    
    print("🏦 LOAN PREDICTION DEMO")
    print("=" * 50)
    
    # Sample applicants with different profiles
    sample_applicants = [
        {
            'name': 'High Income Graduate',
            'data': {
                'Gender': 'Male',
                'Married': 'Yes',
                'Dependents': 1,
                'Education': 'Graduate',
                'Self_Employed': 'No',
                'ApplicantIncome': 8000,
                'CoapplicantIncome': 3000,
                'LoanAmount': 150,
                'Loan_Amount_Term': 360,
                'Credit_History': 1,
                'Property_Area': 'Urban'
            }
        },
        {
            'name': 'Low Income, Poor Credit',
            'data': {
                'Gender': 'Female',
                'Married': 'No',
                'Dependents': 3,
                'Education': 'Not Graduate',
                'Self_Employed': 'Yes',
                'ApplicantIncome': 2500,
                'CoapplicantIncome': 0,
                'LoanAmount': 200,
                'Loan_Amount_Term': 240,
                'Credit_History': 0,
                'Property_Area': 'Rural'
            }
        },
        {
            'name': 'Middle Class Family',
            'data': {
                'Gender': 'Male',
                'Married': 'Yes',
                'Dependents': 2,
                'Education': 'Graduate',
                'Self_Employed': 'No',
                'ApplicantIncome': 5000,
                'CoapplicantIncome': 2500,
                'LoanAmount': 120,
                'Loan_Amount_Term': 360,
                'Credit_History': 1,
                'Property_Area': 'Semiurban'
            }
        },
        {
            'name': 'Self-Employed Entrepreneur',
            'data': {
                'Gender': 'Female',
                'Married': 'Yes',
                'Dependents': 0,
                'Education': 'Graduate',
                'Self_Employed': 'Yes',
                'ApplicantIncome': 6000,
                'CoapplicantIncome': 1500,
                'LoanAmount': 180,
                'Loan_Amount_Term': 300,
                'Credit_History': 1,
                'Property_Area': 'Urban'
            }
        }
    ]
    
    for applicant in sample_applicants:
        print(f"\n📋 Applicant: {applicant['name']}")
        print("-" * 30)
        
        # Show applicant details
        data = applicant['data']
        print(f"Gender: {data['Gender']}, Married: {data['Married']}")
        print(f"Education: {data['Education']}, Dependents: {data['Dependents']}")
        print(f"Income: ${data['ApplicantIncome']:,} + ${data['CoapplicantIncome']:,}")
        print(f"Loan Amount: ${data['LoanAmount']:,}k, Term: {data['Loan_Amount_Term']} months")
        print(f"Credit History: {'Good' if data['Credit_History'] else 'Poor'}")
        print(f"Property Area: {data['Property_Area']}")
        
        # Make prediction
        try:
            result = predictor.predict_loan(data)
            
            print("\n🤖 PREDICTION RESULT:")
            status = "✅ APPROVED" if result['approved'] else "❌ REJECTED"
            print(f"Status: {status}")
            print(f"Approval Probability: {result['probability']:.1%}")
            print(f"Model Used: {result['model_used'].title()}")
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
        
        print("=" * 50)

if __name__ == "__main__":
    demo_predictions()