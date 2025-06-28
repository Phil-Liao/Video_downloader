# Video Downloader Flask Web App

A modern web application for downloading videos from various platforms using yt-dlp (YouTube-DL).

## Features

- **Secure Access**: Family authentication system with security question
- Clean, modern web interface with dark theme
- Support for multiple video platforms (YouTube, Vimeo, Twitter, etc.)
- Automatic file cleanup after download
- Bootstrap-based responsive design
- Real-time download feedback
- Session management with login/logout functionality

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Important:** If you encounter YouTube bot detection errors, set up browser cookies:

   **Option A - Automatic (Chrome only):**

   ```bash
   python extract_cookies.py
   ```

   **Option B - Manual:**

   - Install a browser extension like "Get cookies.txt LOCALLY" or "cookies.txt"
   - Go to YouTube.com while logged in - Export cookies for youtube.com domain
   - Save as `cookies.firefox-private.txt` in the app directory

3. Run the application:

   **For Local Development:**

   ```bash
   python main.py
   ```

   **For Production Deployment (PythonAnywhere):**
   See `DEPLOYMENT.md` for detailed instructions.

4. Open your browser and navigate to: `http://localhost:8080` (local) or your PythonAnywhere URL

5. **Login**: You'll be prompted with a security question. Enter the correct answer to access the video downloader.

## Authentication

The application includes a family security system:

- **Security Question**: "What is your home town?"
- **Correct Answer**: "douliou"
- **Session Management**: Once logged in, you'll remain authenticated until you logout or close the browser
- **Logout**: Click the logout button in the top-right corner to end your session

## Usage

1. Enter the URL of the video you want to download
2. Click the "Download Video" button
3. The video will be processed and automatically downloaded to your browser

## File Structure

```
Video_downloader/
├── main.py                      # Flask application
├── wsgi.py                      # WSGI configuration for deployment
├── requirements.txt             # Python dependencies
├── extract_cookies.py           # Cookie extraction helper
├── DEPLOYMENT.md                # PythonAnywhere deployment guide
├── cookies.firefox-private.txt  # Browser cookies (optional)
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── index.html              # Main page template
│   └── login.html              # Login page template
├── static/                     # Static files (CSS, JS, images)
└── video_files/                # Temporary video storage
```

## Configuration

You can modify the following settings in `main.py`:

- **Port**: Change the port number (default: 5000)
- **Host**: Change the host (default: 0.0.0.0 for all interfaces)
- **Secret Key**: Change the Flask secret key for security
- **Download Options**: Modify yt-dlp options in the `download_video()` function

## Supported Platforms

This application supports all platforms that yt-dlp supports, including:

- YouTube
- Vimeo
- Twitter
- Facebook
- Instagram
- And many more...

## Security Notes

1. Change the secret key in `main.py` before deploying to production
2. Consider adding rate limiting for production use
3. Be aware of the legal implications of downloading copyrighted content

## Troubleshooting

### Common Issues and Solutions

1. **"Sign in to confirm you're not a bot" Error**

   - **Cause**: YouTube's bot detection system
   - **Solution**: Extract and use browser cookies (see setup instructions above)
   - **Alternative**: Wait 15-30 minutes and try again

2. **Import errors**:

   - Make sure all dependencies are installed with `pip install -r requirements.txt`

3. **Download failures**:

   - Check if the URL is valid and publicly accessible
   - Try the video URL directly in your browser first

4. **Cookie issues**:

   - Ensure your cookie file is in the correct Netscape format
   - Re-export cookies if they're older than a few days
   - Make sure you're logged into YouTube when exporting cookies

5. **Age-restricted videos**:

   - These require valid browser cookies from a logged-in session
   - Use the cookie extraction method above

6. **Port already in use**:
   - Change the port number in `main.py` and `run.py`
   - Or stop other applications using port 8080

## Migration from Streamlit

This Flask version provides the same functionality as the original Streamlit app but with:

- Better performance for concurrent users
- More customizable UI
- Standard web server deployment options
- Improved file handling and cleanup
