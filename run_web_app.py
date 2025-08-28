#!/usr/bin/env python3
"""
Launch script for the Loan Prediction Web Application
"""

import subprocess
import sys
import webbrowser
import time
from urllib.request import urlopen
from urllib.error import URLError

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please install: pip install Flask flask-cors")
        return False

def wait_for_server(url="http://localhost:5000", timeout=30):
    """Wait for the server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            urlopen(url)
            return True
        except URLError:
            time.sleep(0.5)
    return False

def main():
    print("🚀 Loan Prediction Web Application Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Start the web application
    print("🔄 Starting web server...")
    try:
        # Run the Flask app
        from app import app
        print("✅ Server starting at http://localhost:5000")
        print("\n📝 Instructions:")
        print("1. Open http://localhost:5000 in your browser")
        print("2. Fill in the loan application form")
        print("3. Click 'Get Prediction' to see results")
        print("4. Press Ctrl+C to stop the server")
        print("\n" + "=" * 50)
        
        # Try to open browser automatically
        try:
            time.sleep(1)  # Give server time to start
            webbrowser.open('http://localhost:5000')
            print("🌐 Browser opened automatically")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("Please manually open http://localhost:5000")
        
        # Start the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)