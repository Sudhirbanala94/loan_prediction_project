# 🏦 Loan Prediction System

A comprehensive machine learning application that predicts loan approval decisions with both CLI and web interfaces.

## ✨ Features

- **🌐 Web Application**: Professional web interface with modern UI/UX
- **🤖 Multi-Model ML**: Tests 4 different ML algorithms (Random Forest, Gradient Boosting, Logistic Regression, SVM)
- **🎯 Automatic Model Selection**: Picks the best-performing model
- **💻 Interactive Prediction**: Both CLI and web interfaces
- **🔧 Data Preprocessing**: Handles missing values, feature engineering
- **💾 Model Persistence**: Save/load trained models
- **🧪 Comprehensive Testing**: Unit tests and performance validation
- **📱 Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### 🌐 Web Application (Recommended)
```bash
# Install dependencies
pip install Flask flask-cors pandas scikit-learn numpy joblib

# Launch web application
python3 run_web_app.py

# Open browser to http://localhost:5000
```

### 💻 Command Line Interface
```bash
# Navigate to project directory
cd loan_prediction_project

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Interactive Mode (Manual Input)
```bash
python src/loan_predictor/loan_predictor.py
```

#### 2. Demo Mode (Automated Examples)
```bash
python src/demo_prediction.py
```

#### 3. Run Tests
```bash
python tests/simple_tests.py
```

## 📁 Project Structure

```
loan_prediction_project/
├── src/
│   ├── loan_predictor/
│   │   ├── __init__.py
│   │   └── loan_predictor.py      # Core ML application
│   └── demo_prediction.py         # Demo with sample data
├── tests/
│   ├── simple_tests.py            # Basic functionality tests
│   └── test_loan_predictor.py     # Unit tests
├── examples/
│   ├── enhanced_features_example.py
│   ├── advanced_models_example.py
│   ├── model_explanation_example.py
│   └── editing_guide.py           # How to modify the system
├── models/
│   └── *.pkl                      # Saved trained models
├── data/                          # For future data files
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 📊 Model Performance

- **Accuracy**: 85-95% on test data
- **Best Model**: Usually Random Forest or Gradient Boosting
- **Training Time**: ~10 seconds on 1000 samples
- **Prediction Time**: ~1ms per prediction

## 🔧 Key Input Features

| Feature | Type | Example | Impact |
|---------|------|---------|---------|
| Credit History | 0/1 | 1 | High |
| Income | Number | 5000 | High |
| Loan Amount | Number | 150 | Medium |
| Education | Text | Graduate | Medium |
| Employment | Text | No | Low |

## 🎯 Example Predictions

**✅ Approved**: High income graduate with good credit
**❌ Rejected**: Low income, poor credit, many dependents

## 🛠️ Development

### Adding New Features
See `examples/enhanced_features_example.py` for examples.

### Adding New Models
See `examples/advanced_models_example.py` for examples.

### Testing
```bash
# Run all tests
python tests/simple_tests.py

# Run specific test
python tests/test_loan_predictor.py
```

## 📈 Future Enhancements

- [ ] Web API (Flask/FastAPI)
- [ ] Database integration
- [ ] Real-time model monitoring
- [ ] Model explainability dashboard
- [ ] A/B testing framework

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details.