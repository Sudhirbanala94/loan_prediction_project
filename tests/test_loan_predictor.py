#!/usr/bin/env python3

import unittest
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from loan_predictor.loan_predictor import LoanPredictor

class TestLoanPredictor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.predictor = LoanPredictor()
        
    def test_sample_data_generation(self):
        """Test that sample data is generated correctly"""
        data = self.predictor.create_sample_data(100)
        
        # Check data shape
        self.assertEqual(data.shape[0], 100)
        self.assertEqual(data.shape[1], 12)  # 11 features + 1 target
        
        # Check required columns exist
        required_cols = ['Gender', 'ApplicantIncome', 'LoanAmount', 'Loan_Status']
        for col in required_cols:
            self.assertIn(col, data.columns)
        
        # Check data types and ranges
        self.assertTrue(data['ApplicantIncome'].min() > 0)
        self.assertTrue(data['LoanAmount'].min() > 0)
        self.assertIn(data['Loan_Status'].iloc[0], ['Y', 'N'])
    
    def test_preprocessing(self):
        """Test data preprocessing pipeline"""
        # Create test data with missing values
        test_data = pd.DataFrame({
            'Gender': ['Male', None, 'Female'],
            'ApplicantIncome': [5000, 6000, None],
            'LoanAmount': [100, None, 150],
            'Credit_History': [1, 0, None]
        })
        
        processed = self.predictor.preprocess_data(test_data)
        
        # Check no missing values remain
        self.assertEqual(processed.isnull().sum().sum(), 0)
        
        # Check derived features exist
        self.assertIn('Total_Income', processed.columns)
        self.assertIn('Income_to_Loan_Ratio', processed.columns)
    
    def test_feature_encoding(self):
        """Test categorical feature encoding"""
        test_data = pd.DataFrame({
            'Gender': ['Male', 'Female', 'Male'],
            'Education': ['Graduate', 'Not Graduate', 'Graduate']
        })
        
        encoded = self.predictor.encode_features(test_data, fit=True)
        
        # Check that categorical columns are now numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(encoded['Gender']))
        self.assertTrue(pd.api.types.is_numeric_dtype(encoded['Education']))
        
        # Check encoding values are valid
        self.assertTrue(encoded['Gender'].isin([0, 1]).all())
    
    def test_prediction_format(self):
        """Test that predictions return correct format"""
        # Train on small sample
        sample_data = self.predictor.create_sample_data(50)
        self.predictor.train_models(sample_data)
        
        # Test prediction
        test_applicant = {
            'Gender': 'Male',
            'Married': 'Yes',
            'Dependents': 1,
            'Education': 'Graduate',
            'Self_Employed': 'No',
            'ApplicantIncome': 5000,
            'CoapplicantIncome': 2000,
            'LoanAmount': 120,
            'Loan_Amount_Term': 360,
            'Credit_History': 1,
            'Property_Area': 'Urban'
        }
        
        result = self.predictor.predict_loan(test_applicant)
        
        # Check result format
        self.assertIn('approved', result)
        self.assertIn('probability', result)
        self.assertIn('model_used', result)
        self.assertIsInstance(result['approved'], bool)
        self.assertIsInstance(result['probability'], float)
        self.assertTrue(0 <= result['probability'] <= 1)
    
    def test_model_performance(self):
        """Test that model achieves reasonable performance"""
        # Train on larger sample
        sample_data = self.predictor.create_sample_data(500)
        results = self.predictor.train_models(sample_data)
        
        # Check that at least one model achieves > 80% accuracy
        best_accuracy = max(results.values())
        self.assertGreater(best_accuracy, 0.8, "Model accuracy too low")
        
        # Check that best model is selected
        self.assertIsNotNone(self.predictor.best_model)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        
        # Test with extreme values
        extreme_applicant = {
            'Gender': 'Male',
            'Married': 'Yes',
            'Dependents': 0,
            'Education': 'Graduate',
            'Self_Employed': 'No',
            'ApplicantIncome': 999999,  # Very high income
            'CoapplicantIncome': 0,
            'LoanAmount': 1,  # Very small loan
            'Loan_Amount_Term': 360,
            'Credit_History': 1,
            'Property_Area': 'Urban'
        }
        
        # Train first
        sample_data = self.predictor.create_sample_data(100)
        self.predictor.train_models(sample_data)
        
        # Should handle extreme values without error
        result = self.predictor.predict_loan(extreme_applicant)
        self.assertIsNotNone(result)

class TestModelComparison(unittest.TestCase):
    """Test different aspects of model performance"""
    
    def test_model_consistency(self):
        """Test that predictions are consistent for same input"""
        predictor = LoanPredictor()
        sample_data = predictor.create_sample_data(200)
        predictor.train_models(sample_data)
        
        test_applicant = {
            'Gender': 'Female',
            'Married': 'No',
            'Dependents': 2,
            'Education': 'Graduate',
            'Self_Employed': 'Yes',
            'ApplicantIncome': 4000,
            'CoapplicantIncome': 1000,
            'LoanAmount': 100,
            'Loan_Amount_Term': 240,
            'Credit_History': 1,
            'Property_Area': 'Semiurban'
        }
        
        # Make multiple predictions
        result1 = predictor.predict_loan(test_applicant)
        result2 = predictor.predict_loan(test_applicant)
        
        # Results should be identical
        self.assertEqual(result1['approved'], result2['approved'])
        self.assertEqual(result1['probability'], result2['probability'])

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)