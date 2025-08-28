#!/usr/bin/env python3

# Example: Enhanced feature engineering
def create_advanced_features(df):
    """Add more sophisticated features"""
    
    # 1. Debt-to-Income Ratio (critical for loan approval)
    df['Debt_to_Income'] = (df['LoanAmount'] * 1000) / (df['ApplicantIncome'] * 12)
    
    # 2. Age-based risk (younger = higher risk)
    df['Age_Group'] = np.random.choice(['Young', 'Middle', 'Senior'], len(df))
    df['Age_Risk_Score'] = df['Age_Group'].map({'Young': 0.3, 'Middle': 0.1, 'Senior': 0.2})
    
    # 3. Employment Stability Score
    df['Employment_Months'] = np.random.randint(1, 120, len(df))
    df['Employment_Stability'] = np.where(df['Employment_Months'] > 24, 1, 0)
    
    # 4. Property Value vs Loan Ratio
    df['Property_Value'] = df['LoanAmount'] * np.random.uniform(1.2, 2.0, len(df))
    df['LTV_Ratio'] = df['LoanAmount'] / df['Property_Value']  # Loan-to-Value
    
    # 5. Monthly Payment Capacity
    df['Monthly_Payment'] = (df['LoanAmount'] * 1000) / df['Loan_Amount_Term']
    df['Payment_to_Income'] = df['Monthly_Payment'] / (df['Total_Income'] / 12)
    
    return df

# Usage in your main code:
# df = create_advanced_features(df)