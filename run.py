#!/usr/bin/env python3
"""
Flask Video Downloader Application
Run this script to start the web server
"""

from main import app

if __name__ == '__main__':
    print("Starting Video Downloader Flask App...")
    print("Open your browser and go to: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=8080)
