#!/usr/bin/env python3
"""
WSGI configuration for Video Downloader Flask App
This file is used for deployment on PythonAnywhere or other WSGI servers.
"""

import sys
import os

# Add your project directory to sys.path
# Update this path to match your actual project directory on PythonAnywhere
# Example: '/home/yourusername/Video_downloader'
project_home = '/home/ipdytdl/Video_downloader'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import your Flask application
from main import app as application

# Ensure the video_files directory exists
os.makedirs(os.path.join(project_home, 'video_files'), exist_ok=True)

if __name__ == "__main__":
    application.run(debug=False)
