#!/usr/bin/env python3

"""
Main entry point for running tests
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from simple_tests import test_basic_functionality, performance_test

if __name__ == "__main__":
    test_basic_functionality()
    performance_test()