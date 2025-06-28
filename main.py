from flask import Flask, request, render_template, send_file, flash, redirect, url_for, session
import yt_dlp as youtube_dl
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-to-a-secure-secret-key-in-production')  # Use environment variable in production

# Production configuration
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def download_video(url):
    # Create a temporary directory for this download
    temp_dir = tempfile.mkdtemp()
    
    # More comprehensive yt-dlp options to avoid bot detection
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'cookiefile': 'cookies.firefox-private.txt' if os.path.exists('cookies.firefox-private.txt') else None,
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,  # Suppress verbose output
        'no_warnings': True,  # Suppress warnings
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        'extractor_args': {
            'youtube': {
                'skip': ['hls', 'dash'],
                'player_client': ['android', 'web'],
            }
        },
        # Try to avoid rate limiting
        'sleep_interval': 1,
        'max_sleep_interval': 5,
        # Format selection - prefer mp4
        'format': 'best[ext=mp4]/mp4/best',
        # Retry options
        'retries': 3,
        'fragment_retries': 3,
        # Ignore errors for unavailable formats
        'ignoreerrors': False,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            title = result.get("title", "video")
            ext = result.get("ext", "mp4")
            
            # Find the actual downloaded file in the temp directory
            # Sometimes the filename differs from what we expect due to sanitization
            downloaded_files = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
            
            if not downloaded_files:
                raise Exception("No file was downloaded")
            
            # Get the first (and likely only) downloaded file
            actual_filename = downloaded_files[0]
            filepath = os.path.join(temp_dir, actual_filename)
            
            # Verify the file actually exists
            if not os.path.exists(filepath):
                raise Exception(f"Downloaded file not found at expected location: {filepath}")
            
            # Create a clean filename for download
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_filename = f"{safe_title}.{ext}" if safe_title else actual_filename
            
            return filepath, safe_filename, title
    except youtube_dl.utils.ExtractorError as e:
        error_msg = str(e)
        if "Sign in to confirm you're not a bot" in error_msg:
            raise Exception("YouTube is blocking the download due to bot detection. Try using browser cookies or try again later.")
        elif "Video unavailable" in error_msg:
            raise Exception("This video is unavailable or private.")
        elif "age-restricted" in error_msg:
            raise Exception("This video is age-restricted. Please provide browser cookies to download it.")
        else:
            raise Exception(f"Video extraction failed: {error_msg}")
    except youtube_dl.utils.DownloadError as e:
        raise Exception(f"Download failed: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm you're not a bot" in error_msg:
            raise Exception("YouTube bot detection triggered. Please try: 1) Using browser cookies, 2) Waiting a few minutes, or 3) Using a different video URL.")
        else:
            raise Exception(f"Error downloading video: {error_msg}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        home_town = request.form.get('home_town', '').strip().lower()
        
        if home_town == 'douliou':
            session['logged_in'] = True
            session['user_name'] = 'Family Member'
            flash('Welcome! You have been logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect answer. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')



@app.route('/download', methods=['POST'])
@login_required
def download():
    url = request.form.get('url', '').strip()
    
    # Basic URL validation
    if not url:
        flash('Please enter a valid URL', 'error')
        return redirect(url_for('index'))
    
    if not (url.startswith('http://') or url.startswith('https://')):
        flash('Please enter a valid URL starting with http:// or https://', 'error')
        return redirect(url_for('index'))
    
    try:
        filepath, filename, title = download_video(url)
        
        # Send the file and clean up after
        def cleanup_file():
            try:
                # Remove the entire temp directory
                temp_dir = os.path.dirname(filepath)
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        
        response = send_file(
            filepath, 
            as_attachment=True, 
            download_name=secure_filename(filename),
            mimetype='video/mp4'
        )
        
        # Schedule cleanup after response is sent
        response.call_on_close(cleanup_file)
        return response
    
    except Exception as e:
        error_msg = str(e)
        # Log more details for file-related errors while keeping user message clean
        if "No such file or directory" in error_msg:
            flash('Download failed: The video file could not be saved properly. Please try again.', 'error')
        else:
            flash(f'Error: {error_msg}', 'error')
        return redirect(url_for('index'))

# Redirect root to login if not authenticated
@app.before_request
def check_login():
    if request.endpoint and request.endpoint != 'login' and request.endpoint != 'static':
        if 'logged_in' not in session or not session['logged_in']:
            if request.endpoint != 'login':
                return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure the video_files directory exists
    os.makedirs('video_files', exist_ok=True)
    app.run(debug=False, host='0.0.0.0', port=8080) 