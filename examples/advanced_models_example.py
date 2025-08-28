#!/usr/bin/env python3

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier  # Need: pip install xgboost
import lightgbm as lgb  # Need: pip install lightgbm

def add_advanced_models(self):
    """Add more sophisticated models to the pipeline"""
    
    advanced_models = {
        # Ensemble Methods
        'extra_trees': ExtraTreesClassifier(random_state=42, n_estimators=100),
        'xgboost': XGBClassifier(random_state=42, eval_metric='logloss'),
        'lightgbm': lgb.LGBMClassifier(random_state=42, verbose=-1),
        
        # Neural Network
        'neural_net': MLPClassifier(
            hidden_layer_sizes=(100, 50),
            random_state=42,
            max_iter=500
        ),
        
        # Probabilistic
        'naive_bayes': GaussianNB(),
    }
    
    # Add to existing models
    self.models.update(advanced_models)
    
    return self.models

# Enhanced Cross-Validation
def enhanced_model_selection(self, X, y):
    """More robust model selection with cross-validation"""
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = {}
    for name, model in self.models.items():
        # 5-fold cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        
        results[name] = {
            'mean_accuracy': cv_scores.mean(),
            'std_accuracy': cv_scores.std(),
            'scores': cv_scores
        }
        
        print(f"{name}: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return results