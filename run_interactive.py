#!/usr/bin/env python3

"""
Main entry point for running the interactive loan prediction system
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from loan_predictor.loan_predictor import main

if __name__ == "__main__":
    main()