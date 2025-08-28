#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

class LoanPredictor:
    def __init__(self):
        self.models = {
            'logistic': LogisticRegression(random_state=42),
            'random_forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'svm': SVC(random_state=42, probability=True)
        }
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.feature_columns = None
        
    def create_sample_data(self, n_samples=1000):
        """Generate sample loan data for demonstration"""
        np.random.seed(42)
        
        data = {
            'Gender': np.random.choice(['Male', 'Female'], n_samples),
            'Married': np.random.choice(['Yes', 'No'], n_samples),
            'Dependents': np.random.choice([0, 1, 2, 3], n_samples),
            'Education': np.random.choice(['Graduate', 'Not Graduate'], n_samples),
            'Self_Employed': np.random.choice(['Yes', 'No'], n_samples),
            'ApplicantIncome': np.random.normal(5000, 2000, n_samples).astype(int),
            'CoapplicantIncome': np.random.normal(2000, 1500, n_samples).astype(int),
            'LoanAmount': np.random.normal(150, 50, n_samples).astype(int),
            'Loan_Amount_Term': np.random.choice([360, 240, 180, 120], n_samples),
            'Credit_History': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
            'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create realistic loan approval logic
        approval_prob = (
            0.3 * (df['Credit_History'] == 1) +
            0.2 * (df['ApplicantIncome'] > 4000) +
            0.1 * (df['Education'] == 'Graduate') +
            0.1 * (df['Married'] == 'Yes') +
            0.1 * (df['Property_Area'] == 'Urban') +
            0.2 * np.random.random(n_samples)
        )
        
        df['Loan_Status'] = np.where(approval_prob > 0.5, 'Y', 'N')
        
        return df
    
    def preprocess_data(self, df):
        """Preprocess the data for training"""
        df = df.copy()
        
        # Handle missing values
        df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
        df['Married'].fillna(df['Married'].mode()[0], inplace=True)
        df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
        df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
        df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0], inplace=True)
        df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
        
        # Create derived features
        df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
        df['Income_to_Loan_Ratio'] = df['Total_Income'] / (df['LoanAmount'] * 1000)
        
        # Handle infinite and very large values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values for numeric columns only
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())
        
        return df
    
    def encode_features(self, df, fit=True):
        """Encode categorical features"""
        df = df.copy()
        categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
        
        for col in categorical_cols:
            if fit:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def train_models(self, df):
        """Train all models and select the best one"""
        print("Preprocessing data...")
        df = self.preprocess_data(df)
        df = self.encode_features(df, fit=True)
        
        # Separate features and target
        X = df.drop(['Loan_Status'], axis=1)
        y = LabelEncoder().fit_transform(df['Loan_Status'])
        
        self.feature_columns = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("\nTraining models...")
        best_score = 0
        results = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            # Train model
            if name in ['logistic', 'svm']:
                model.fit(X_train_scaled, y_train)
                predictions = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
            
            # Evaluate
            accuracy = accuracy_score(y_test, predictions)
            results[name] = accuracy
            
            print(f"{name} accuracy: {accuracy:.4f}")
            
            if accuracy > best_score:
                best_score = accuracy
                self.best_model = (name, model)
        
        print(f"\nBest model: {self.best_model[0]} with accuracy: {best_score:.4f}")
        return results
    
    def predict_loan(self, applicant_data):
        """Predict loan approval for a single applicant"""
        if self.best_model is None:
            raise ValueError("Model not trained yet. Call train_models() first.")
        
        # Convert to DataFrame
        df = pd.DataFrame([applicant_data])
        
        # Preprocess
        df = self.preprocess_data(df)
        df = self.encode_features(df, fit=False)
        
        # Ensure all required columns are present
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        df = df[self.feature_columns]
        
        # Scale if necessary
        model_name, model = self.best_model
        if model_name in ['logistic', 'svm']:
            df_scaled = self.scaler.transform(df)
            prediction = model.predict(df_scaled)[0]
            probability = model.predict_proba(df_scaled)[0]
        else:
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0]
        
        return {
            'approved': bool(prediction),
            'probability': float(probability[1]),  # Probability of approval
            'model_used': model_name
        }
    
    def save_model(self, filename='loan_predictor_model.pkl'):
        """Save the trained model"""
        model_data = {
            'best_model': self.best_model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, filename)
        print(f"Model saved to {filename}")
    
    def load_model(self, filename='loan_predictor_model.pkl'):
        """Load a trained model"""
        model_data = joblib.load(filename)
        self.best_model = model_data['best_model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        print(f"Model loaded from {filename}")

def main():
    predictor = LoanPredictor()
    
    print("Loan Prediction System")
    print("=" * 30)
    
    # Generate sample data and train models
    print("Generating sample data...")
    sample_data = predictor.create_sample_data(1000)
    
    print("Sample data shape:", sample_data.shape)
    print("\nSample data preview:")
    print(sample_data.head())
    
    # Train models
    results = predictor.train_models(sample_data)
    
    # Save model
    predictor.save_model()
    
    print("\n" + "=" * 30)
    print("Interactive Prediction")
    print("=" * 30)
    
    while True:
        try:
            print("\nEnter applicant details (or 'quit' to exit):")
            
            # Get user input
            applicant = {}
            applicant['Gender'] = input("Gender (Male/Female): ").strip()
            if applicant['Gender'].lower() == 'quit':
                break
                
            applicant['Married'] = input("Married (Yes/No): ").strip()
            applicant['Dependents'] = int(input("Number of Dependents (0-3): "))
            applicant['Education'] = input("Education (Graduate/Not Graduate): ").strip()
            applicant['Self_Employed'] = input("Self Employed (Yes/No): ").strip()
            applicant['ApplicantIncome'] = int(input("Applicant Income: "))
            applicant['CoapplicantIncome'] = int(input("Coapplicant Income: "))
            applicant['LoanAmount'] = int(input("Loan Amount (in thousands): "))
            applicant['Loan_Amount_Term'] = int(input("Loan Amount Term (in months): "))
            applicant['Credit_History'] = int(input("Credit History (0/1): "))
            applicant['Property_Area'] = input("Property Area (Urban/Semiurban/Rural): ").strip()
            
            # Make prediction
            result = predictor.predict_loan(applicant)
            
            print("\n" + "-" * 30)
            print("PREDICTION RESULT")
            print("-" * 30)
            print(f"Loan Approved: {'YES' if result['approved'] else 'NO'}")
            print(f"Approval Probability: {result['probability']:.2%}")
            print(f"Model Used: {result['model_used']}")
            print("-" * 30)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please check your input and try again.")

if __name__ == "__main__":
    main()