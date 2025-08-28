#!/usr/bin/env python3

"""
Main entry point for running the loan prediction demo
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from demo_prediction import demo_predictions

if __name__ == "__main__":
    demo_predictions()