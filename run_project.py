import subprocess
import sys
import os
import time
import threading

def log_stream(stream, prefix):
    # Read output line by line and print with prefix
    for line in iter(stream.readline, b''):
        try:
            line_str = line.decode('utf-8', errors='replace').strip()
            if line_str:
                print(f"{prefix} {line_str}")
        except Exception:
            pass

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    backend_script = os.path.join(current_dir, 'backend', 'app.py')
    frontend_script = os.path.join(current_dir, 'frontend', 'server.py')
    
    # Verify scripts exist before spawning
    if not os.path.exists(backend_script):
        print(f"Error: Backend script not found at {backend_script}")
        sys.exit(1)
    if not os.path.exists(frontend_script):
        print(f"Error: Frontend script not found at {frontend_script}")
        sys.exit(1)
        
    print("=" * 60)
    print("  Starting Fake News Detection System (Decoupled)")
    print("=" * 60)
    print("Frontend:    http://localhost:8000")
    print("Backend API: http://localhost:5000")
    print("Press Ctrl+C to terminate both servers.")
    print("=" * 60)
    
    # Spawn Backend
    backend_proc = subprocess.Popen(
        [sys.executable, '-u', backend_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.join(current_dir, 'backend')
    )
    
    # Spawn Frontend
    frontend_proc = subprocess.Popen(
        [sys.executable, '-u', frontend_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.join(current_dir, 'frontend')
    )
    
    # Start background threads to capture and prefix logs
    t1 = threading.Thread(target=log_stream, args=(backend_proc.stdout, "[BACKEND]"), daemon=True)
    t2 = threading.Thread(target=log_stream, args=(backend_proc.stderr, "[BACKEND]"), daemon=True)
    t3 = threading.Thread(target=log_stream, args=(frontend_proc.stdout, "[FRONTEND]"), daemon=True)
    t4 = threading.Thread(target=log_stream, args=(frontend_proc.stderr, "[FRONTEND]"), daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    try:
        while True:
            # Check if either process terminated unexpectedly
            if backend_proc.poll() is not None:
                print(f"[SYSTEM] Backend stopped with code {backend_proc.poll()}")
                break
            if frontend_proc.poll() is not None:
                print(f"[SYSTEM] Frontend stopped with code {frontend_proc.poll()}")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Ctrl+C detected. Terminating servers...")
    finally:
        # Terminate processes gracefully
        backend_proc.terminate()
        frontend_proc.terminate()
        
        # Give them a moment to close
        time.sleep(1)
        
        # Kill if still alive
        if backend_proc.poll() is None:
            backend_proc.kill()
        if frontend_proc.poll() is None:
            frontend_proc.kill()
            
        print("[SYSTEM] Both servers stopped successfully.")
