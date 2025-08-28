#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance

def explain_prediction(self, applicant_data):
    """Explain why a loan was approved/rejected"""
    
    # Make prediction first
    result = self.predict_loan(applicant_data)
    
    # Get feature importance (for tree-based models)
    if self.best_model[0] in ['random_forest', 'gradient_boosting']:
        model = self.best_model[1]
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n📊 TOP FACTORS INFLUENCING DECISION:")
        print("-" * 40)
        for i, row in feature_importance.head(5).iterrows():
            print(f"{row['feature']}: {row['importance']:.3f}")
    
    # Show what would improve approval chances
    improvement_suggestions = []
    
    if applicant_data['Credit_History'] == 0:
        improvement_suggestions.append("🔸 Improve credit history")
    
    if applicant_data['ApplicantIncome'] < 4000:
        improvement_suggestions.append("🔸 Increase income or add co-applicant")
    
    if applicant_data['Education'] == 'Not Graduate':
        improvement_suggestions.append("🔸 Educational qualification helps")
    
    if improvement_suggestions:
        print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
        for suggestion in improvement_suggestions:
            print(f"   {suggestion}")
    
    return result

def visualize_feature_importance(self):
    """Create visualization of feature importance"""
    if self.best_model[0] in ['random_forest', 'gradient_boosting']:
        model = self.best_model[1]
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=True)
        
        plt.figure(figsize=(10, 6))
        plt.barh(importance_df['feature'], importance_df['importance'])
        plt.title('Feature Importance in Loan Prediction')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.savefig('feature_importance.png')
        plt.show()
        
        return importance_df