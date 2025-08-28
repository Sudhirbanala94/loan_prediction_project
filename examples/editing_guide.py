#!/usr/bin/env python3

"""
LOAN PREDICTOR EDITING GUIDE
============================

Here are common modifications you might want to make:

1. CHANGE APPROVAL LOGIC
------------------------
Edit create_sample_data() function around line 40:

OLD:
approval_prob = (
    0.3 * (df['Credit_History'] == 1) +
    0.2 * (df['ApplicantIncome'] > 4000) +
    ...
)

NEW (stricter criteria):
approval_prob = (
    0.4 * (df['Credit_History'] == 1) +        # Credit history more important
    0.3 * (df['ApplicantIncome'] > 6000) +     # Higher income threshold
    0.2 * (df['Education'] == 'Graduate') +
    0.1 * (df['Married'] == 'Yes')
)

2. ADD NEW FEATURES
-------------------
In preprocess_data() function around line 75:

# Add after existing derived features:
df['Loan_Income_Ratio'] = df['LoanAmount'] * 1000 / df['Total_Income']
df['High_Income'] = (df['ApplicantIncome'] > 7000).astype(int)
df['Large_Loan'] = (df['LoanAmount'] > 200).astype(int)

3. CHANGE MODEL SELECTION
-------------------------
In __init__() method around line 18:

# Remove models you don't want:
self.models = {
    'random_forest': RandomForestClassifier(random_state=42, n_estimators=200),  # More trees
    'gradient_boosting': GradientBoostingClassifier(random_state=42, n_estimators=200),
    # Remove: 'logistic': LogisticRegression(random_state=42),
    # Remove: 'svm': SVC(random_state=42, probability=True)
}

4. ADJUST HYPERPARAMETERS
-------------------------
self.models = {
    'random_forest': RandomForestClassifier(
        random_state=42, 
        n_estimators=200,           # More trees for better performance
        max_depth=10,               # Prevent overfitting
        min_samples_split=5,        # Minimum samples to split
        class_weight='balanced'     # Handle imbalanced data
    ),
}

5. CHANGE PREDICTION THRESHOLD
------------------------------
In predict_loan() method around line 180:

OLD:
prediction = model.predict(df_scaled)[0]

NEW (custom threshold):
probabilities = model.predict_proba(df_scaled)[0]
prediction = 1 if probabilities[1] > 0.7 else 0  # 70% threshold instead of 50%

6. ADD DATA VALIDATION
----------------------
Add at the beginning of predict_loan():

def validate_applicant_data(self, data):
    required_fields = ['Gender', 'ApplicantIncome', 'LoanAmount', 'Credit_History']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if data['ApplicantIncome'] <= 0:
        raise ValueError("Income must be positive")
    
    if data['LoanAmount'] <= 0:
        raise ValueError("Loan amount must be positive")

7. CHANGE OUTPUT FORMAT
-----------------------
In predict_loan() method, change the return statement:

return {
    'approved': bool(prediction),
    'probability': float(probability[1]),
    'confidence': 'High' if abs(probability[1] - 0.5) > 0.3 else 'Low',
    'recommendation': self._get_recommendation(applicant_data, probability[1]),
    'model_used': model_name
}

STEP-BY-STEP EDITING PROCESS:
=============================

1. Make a backup copy:
   cp loan_predictor.py loan_predictor_backup.py

2. Edit the file:
   nano loan_predictor.py  # or your preferred editor

3. Test your changes:
   python3 simple_tests.py

4. If tests pass, test with real data:
   python3 demo_prediction.py

5. If something breaks, restore backup:
   cp loan_predictor_backup.py loan_predictor.py
"""

# Example: Enhanced version with multiple improvements
class EnhancedLoanPredictor:
    """Enhanced version with additional features"""
    
    def __init__(self):
        # More sophisticated models
        self.models = {
            'random_forest_optimized': RandomForestClassifier(
                random_state=42, 
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                class_weight='balanced'
            ),
            'gradient_boosting_optimized': GradientBoostingClassifier(
                random_state=42,
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6
            )
        }
        
    def advanced_feature_engineering(self, df):
        """Create more sophisticated features"""
        # Existing features
        df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
        df['Income_to_Loan_Ratio'] = df['Total_Income'] / (df['LoanAmount'] * 1000)
        
        # New advanced features
        df['Monthly_Payment'] = (df['LoanAmount'] * 1000) / df['Loan_Amount_Term']
        df['Payment_to_Income_Ratio'] = df['Monthly_Payment'] / (df['Total_Income'] / 12)
        df['High_Income_Flag'] = (df['ApplicantIncome'] > df['ApplicantIncome'].quantile(0.75)).astype(int)
        df['Risk_Score'] = (
            0.3 * (1 - df['Credit_History']) +  # Bad credit increases risk
            0.2 * (df['Payment_to_Income_Ratio'] > 0.4).astype(int) +  # High payment ratio
            0.2 * (df['Self_Employed'] == 'Yes').astype(int) +  # Self-employment risk
            0.3 * (df['Dependents'] > 2).astype(int)  # Many dependents
        )
        
        return df