# PythonAnywhere Deployment Guide

## Prerequisites

- PythonAnywhere account
- Basic understanding of web app deployment

## Step-by-Step Deployment Instructions

### 1. Upload Your Files

Upload all your project files to PythonAnywhere using one of these methods:

**Option A: Using Git (Recommended)**

```bash
# In PythonAnywhere console
cd ~
git clone <your-repo-url>
cd Video_downloader
```

**Option B: File Upload**

- Use the Files tab in PythonAnywhere dashboard
- Upload all files to `/home/yourusername/Video_downloader/`

### 2. Install Dependencies

In the PythonAnywhere console:

```bash
cd ~/Video_downloader
pip3.10 install --user -r requirements.txt
```

### 3. Configure Web App

1. Go to the **Web** tab in your PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10**

### 4. Configure WSGI File

1. In the Web tab, click on the **WSGI configuration file** link
2. Replace the entire content with:

```python
#!/usr/bin/env python3
import sys
import os

# Update this path to match your username and project location
project_home = '/home/YOURUSERNAME/Video_downloader'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import your Flask application
from main import app as application

# Ensure the video_files directory exists
os.makedirs(os.path.join(project_home, 'video_files'), exist_ok=True)

if __name__ == "__main__":
    application.run(debug=False)
```

**Important**: Replace `YOURUSERNAME` with your actual PythonAnywhere username!

### 5. Configure Static Files (Optional)

If you have static files, add this in the Web tab:

- URL: `/static/`
- Directory: `/home/yourusername/Video_downloader/static/`

### 6. Set Environment Variables

In the Web tab, under **"Environment variables"**, add:

- `FLASK_ENV`: `production`

### 7. Update Secret Key

Edit your `main.py` file and change the secret key:

```python
app.secret_key = 'your-super-secret-production-key-here'
```

### 8. Test Your App

1. Click **"Reload"** in the Web tab
2. Visit your app at: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Common Issues:

1. **Import Errors**

   - Check that all dependencies are installed with `--user` flag
   - Verify the project path in WSGI file is correct

2. **Permission Errors**

   - Ensure the `video_files` directory has write permissions
   - Check file ownership and permissions

3. **Static Files Not Loading**

   - Configure static files mapping in Web tab
   - Check static file paths

4. **Session Issues**
   - Make sure secret key is set properly
   - Check that sessions are working in production

### Log Files

Check these locations for error logs:

- Error log: Web tab → "Log files" → Error log
- Server log: Web tab → "Log files" → Server log

## Security Notes for Production

1. **Change Secret Key**: Use a strong, unique secret key
2. **Debug Mode**: Ensure debug is set to False in production
3. **Cookie Security**: Consider adding secure cookie settings
4. **Rate Limiting**: Consider implementing rate limiting for login attempts

## File Structure on PythonAnywhere

```
/home/yourusername/Video_downloader/
├── main.py
├── wsgi.py
├── requirements.txt
├── extract_cookies.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── login.html
├── static/ (if any)
├── video_files/ (created automatically)
└── cookies.firefox-private.txt (optional)
```

## Updating Your App

To update your deployed app:

1. Make changes to your files
2. Upload/sync the changes
3. Click **"Reload"** in the Web tab

That's it! Your video downloader should now be live on PythonAnywhere.
