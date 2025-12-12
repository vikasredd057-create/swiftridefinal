
import subprocess
import sys
import time
import os
import signal

def run_gateway():
    print("=" * 60)
    print("SwiftRide Unified Gateway System")
    print("=" * 60)
    
    processes = []
    
    # Open log files
    backend_log = open("backend_service.log", "w")
    gateway_log = open("gateway_service.log", "w")
    
    try:
        # 1. Start Backend Service
        print("Starting Backend Service on Port 8001...")
        backend_cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend_service.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8001"
        ]
        
        backend_proc = subprocess.Popen(
            backend_cmd,
            stdout=backend_log,
            stderr=subprocess.STDOUT,
            creationflags=0 # No new console, capture output
        )
        processes.append(backend_proc)
        time.sleep(2) # Wait for backend startup
        
        # 2. Start Gateway Service
        print("Starting Gateway Service on Port 7000...")
        gateway_cmd = [
            sys.executable, "-m", "uvicorn", 
            "gateway_service.main:app", 
            "--host", "0.0.0.0", 
            "--port", "7000"
        ]
        
        gateway_proc = subprocess.Popen(
            gateway_cmd,
            stdout=gateway_log,
            stderr=subprocess.STDOUT,
            creationflags=0
        )
        processes.append(gateway_proc)
        
        print("\n" + "=" * 60)
        print("SYSTEM READY!")
        print("Access the Admin/Gateway here: http://localhost:7000")
        print("=" * 60)
        print("Press Ctrl+C to shutdown network.")
        
        # Monitor Loop
        while True:
            time.sleep(1)
            # Check if processes are alive
            if backend_proc.poll() is not None:
                print("Backend service died unexpectedly! Check backend_service.log")
                break
            if gateway_proc.poll() is not None:
                print("Gateway service died unexpectedly! Check gateway_service.log")
                break
                
    except KeyboardInterrupt:
        print("\nShutting down system...")
    finally:
        for p in processes:
            try:
                p.terminate()
            except:
                pass
        
        # Close logs
        try:
            backend_log.close()
            gateway_log.close()
        except:
            pass
            
        print("Shutdown complete.")

if __name__ == "__main__":
    run_gateway()
