"""
Script to run all three microservices simultaneously.
"""
import subprocess
import sys
import time

def run_services():
    print("Starting SwiftRide Microservices...")
    print("=" * 60)
    
    services = [
        {
            "name": "Backend Service",
            "command": [sys.executable, "-m", "uvicorn", "backend_service.main:app", "--host", "0.0.0.0", "--port", "8001"],
            "port": 8001
        },
        {
            "name": "User Service",
            "command": [sys.executable, "-m", "uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8000"],
            "port": 8000
        },
        {
            "name": "Driver Service",
            "command": [sys.executable, "-m", "uvicorn", "driver_service.main:app", "--host", "0.0.0.0", "--port", "8002"],
            "port": 8002
        }
    ]
    
    processes = []
    
    try:
        for service in services:
            print(f"\nStarting {service['name']} on port {service['port']}...")
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            processes.append(process)
            time.sleep(2)  # Wait a bit between starting services
        
        print("\n" + "=" * 60)
        print("All services started successfully!")
        print("\nService URLs:")
        print("   User Service:    http://localhost:8000")
        print("   Backend Service: http://localhost:8001")
        print("   Driver Service:  http://localhost:8002")
        print("\nPress Ctrl+C to stop all services")
        print("=" * 60)
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping all services...")
        for process in processes:
            process.terminate()
        print("All services stopped")
        
    except Exception as e:
        print(f"\nError: {e}")
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    run_services()
