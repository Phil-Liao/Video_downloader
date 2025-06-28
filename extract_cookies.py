#!/usr/bin/env python3
"""
Cookie Extraction Helper
This script helps extract cookies from your browser for use with the video downloader.
"""

import os
import json
import sqlite3
from pathlib import Path

def extract_chrome_cookies():
    """Extract cookies from Chrome browser"""
    print("Extracting cookies from Chrome...")
    
    # Chrome cookie locations for different OS
    chrome_paths = {
        'darwin': '~/Library/Application Support/Google/Chrome/Default/Cookies',  # macOS
        'linux': '~/.config/google-chrome/Default/Cookies',  # Linux
        'win32': '~/AppData/Local/Google/Chrome/User Data/Default/Cookies'  # Windows
    }
    
    import sys
    platform = sys.platform
    if platform.startswith('win'):
        platform = 'win32'
    
    cookie_path = Path(chrome_paths.get(platform, '')).expanduser()
    
    if not cookie_path.exists():
        print(f"Chrome cookies not found at: {cookie_path}")
        return False
    
    try:
        # Copy the cookies file (Chrome locks it)
        import shutil
        temp_cookie_path = Path('temp_cookies.db')
        shutil.copy2(cookie_path, temp_cookie_path)
        
        # Connect to the cookies database
        conn = sqlite3.connect(temp_cookie_path)
        cursor = conn.cursor()
        
        # Extract YouTube cookies
        cursor.execute("""
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
            FROM cookies 
            WHERE host_key LIKE '%youtube%' OR host_key LIKE '%google%'
        """)
        
        cookies = cursor.fetchall()
        conn.close()
        
        # Write cookies in Netscape format
        with open('cookies.firefox-private.txt', 'w') as f:
            f.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                host, name, value, path, expires, secure, httponly = cookie
                if expires:
                    f.write(f"{host}\tTRUE\t{path}\t{'TRUE' if secure else 'FALSE'}\t{expires//1000000}\t{name}\t{value}\n")
        
        # Clean up
        temp_cookie_path.unlink()
        
        print("✅ Cookies extracted successfully to cookies.firefox-private.txt")
        return True
        
    except Exception as e:
        print(f"❌ Error extracting cookies: {e}")
        if Path('temp_cookies.db').exists():
            Path('temp_cookies.db').unlink()
        return False

def manual_cookie_instructions():
    """Provide manual instructions for cookie extraction"""
    print("\n" + "="*60)
    print("MANUAL COOKIE EXTRACTION INSTRUCTIONS")
    print("="*60)
    print("""
1. Install a browser extension:
   - Chrome: "Get cookies.txt LOCALLY" or "cookies.txt"
   - Firefox: "cookies.txt" extension

2. Go to YouTube.com and make sure you're logged in

3. Use the extension to export cookies:
   - Click the extension icon
   - Select "Export" or "Download"
   - Choose "youtube.com" domain
   - Save as "cookies.firefox-private.txt" in this app directory

4. Restart the video downloader app

Alternative method (Advanced users):
- Use browser developer tools (F12)
- Go to Application/Storage tab
- Copy cookies manually from youtube.com domain
- Format them in Netscape cookie format
""")

if __name__ == '__main__':
    print("🍪 Video Downloader Cookie Helper")
    print("-" * 40)
    
    print("\n1. Automatic extraction (Chrome only)")
    print("2. Manual extraction instructions")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        success = extract_chrome_cookies()
        if not success:
            print("\nAutomatic extraction failed. Showing manual instructions...")
            manual_cookie_instructions()
    elif choice == '2':
        manual_cookie_instructions()
    else:
        print("Invalid choice. Showing manual instructions...")
        manual_cookie_instructions()
    
    print("\n" + "="*60)
    print("After setting up cookies, restart your video downloader!")
    print("="*60)
