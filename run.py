import os
import sys
import subprocess
import webbrowser
import time

def get_python_exe():
    if os.path.exists(r"C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe"):
        return r"C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe"
    return sys.executable

def check_dependencies():
    py_exe = get_python_exe()
    
    # Ensure site-packages are added
    site_pkg = os.path.expanduser(r"~\AppData\Roaming\Python\Python313\site-packages")
    if os.path.exists(site_pkg) and site_pkg not in sys.path:
        sys.path.insert(0, site_pkg)

    required = ['flask', 'flask_cors', 'pandas', 'numpy', 'sklearn']
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}...")
        req_file = os.path.join(os.path.dirname(__file__), 'backend', 'requirements.txt')
        subprocess.check_call([py_exe, '-m', 'pip', 'install', '--user', '-r', req_file])

def main():
    print("==================================================")
    print("Starting AI Study Tracker Platform...")
    print("==================================================")
    
    check_dependencies()
    
    backend_script = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')
    py_exe = get_python_exe()
    
    print("\nStarting Backend REST API & Serving Frontend UI...")
    print("Web Application running at: http://localhost:5000\n")
    
    def open_browser():
        time.sleep(1.5)
        try:
            webbrowser.open('http://localhost:5000')
        except Exception:
            pass

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    subprocess.run([py_exe, backend_script])

if __name__ == '__main__':
    main()
