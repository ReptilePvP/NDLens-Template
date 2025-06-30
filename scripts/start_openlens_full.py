#!/usr/bin/env python
"""
OpenLens Full Startup Script
Starts both the API server and web interface
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import http.server
import socketserver
from pathlib import Path

# Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000
WEB_HOST = "127.0.0.1"
WEB_PORT = 3000
WEB_FILE = "index.html"

# Get the project root directory
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
WEB_DIR = PROJECT_ROOT / "web"

class WebServerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from web directory"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_api_server():
    """Start the FastAPI server"""
    print(f"🚀 Starting OpenLens API server on http://{API_HOST}:{API_PORT}")
    
    # Change to src directory and add it to Python path
    original_cwd = os.getcwd()
    os.chdir(SRC_DIR)
    sys.path.insert(0, str(SRC_DIR))
    
    try:
        import uvicorn
        from main import app
        
        uvicorn.run(
            app, 
            host=API_HOST, 
            port=API_PORT,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        os.chdir(original_cwd)
        sys.exit(1)

def start_web_server():
    """Start the web interface server"""
    print(f"🌐 Starting web interface server on http://{WEB_HOST}:{WEB_PORT}")
    try:
        with socketserver.TCPServer((WEB_HOST, WEB_PORT), WebServerHandler) as httpd:
            print(f"📁 Serving files from: {WEB_DIR}")
            print(f"🔗 Web interface URL: http://{WEB_HOST}:{WEB_PORT}/{WEB_FILE}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        sys.exit(1)

def check_dependencies():
    """Check if required files exist"""
    required_files = [
        SRC_DIR / "main.py",
        WEB_DIR / "index.html",
        SRC_DIR / "selenium_lens_scraper.py",
        SRC_DIR / "bs4_small_scraper.py",
        SRC_DIR / "llm_analysis.py",
        SRC_DIR / "config.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not file.exists():
            missing_files.append(str(file.relative_to(PROJECT_ROOT)))
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def wait_for_server(host, port, timeout=30):
    """Wait for server to start"""
    import socket
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(1)
    return False

def open_browser():
    """Open the web interface in default browser"""
    time.sleep(3)  # Wait a bit for servers to start
    
    # Check if API server is running
    if wait_for_server(API_HOST, API_PORT, 10):
        print(f"✅ API server is ready at http://{API_HOST}:{API_PORT}")
    else:
        print(f"⚠️  API server may not be ready yet")
    
    # Check if web server is running
    if wait_for_server(WEB_HOST, WEB_PORT, 10):
        print(f"✅ Web server is ready at http://{WEB_HOST}:{WEB_PORT}")
        url = f"http://{WEB_HOST}:{WEB_PORT}/{WEB_FILE}"
        print(f"🌐 Opening web interface: {url}")
        webbrowser.open(url)
    else:
        print(f"⚠️  Web server may not be ready yet")

def main():
    """Main function to start both servers"""
    print("🔍 OpenLens - Starting Full Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start - missing required files")
        sys.exit(1)
    
    print("✅ All required files found")
    
    try:
        # Start API server in a separate thread
        api_thread = threading.Thread(target=start_api_server, daemon=True)
        api_thread.start()
        
        # Start browser opening in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start web server in main thread (this will block)
        start_web_server()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down OpenLens...")
        print("Thanks for using OpenLens! 👋")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
