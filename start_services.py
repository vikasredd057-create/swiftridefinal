"""
SwiftRide - Background Service Launcher
Runs all services in a single window with background processes
"""
import subprocess
import sys
import time
import os

def start_service_background(name, port, command, env_vars=None):
    """Start a service in the background"""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    print(f"[OK] {name} started on port {port}")
    return process

def main():
    print("=" * 60)
    print("SwiftRide - Starting All Services")
    print("=" * 60)
    print()
    
    processes = []
    
    try:
        # Start Backend Service
        print("Starting Backend Service (Port 8001)...")
        p1 = start_service_background(
            "Backend Service", 8001,
            [sys.executable, "-m", "uvicorn", "backend_service.main:app", 
             "--host", "0.0.0.0", "--port", "8001"]
        )
        processes.append(p1)
        time.sleep(3)
        
        # Start User Service
        print("Starting User Service (Port 8000)...")
        p2 = start_service_background(
            "User Service", 8000,
            [sys.executable, "-m", "uvicorn", "user_service.main:app", 
             "--host", "0.0.0.0", "--port", "8000"]
        )
        processes.append(p2)
        time.sleep(2)
        
        # Start Driver Instances
        drivers = [
            {"id": 1, "name": "Rajesh Kumar", "port": 9001},
            {"id": 2, "name": "Amit Singh", "port": 9002},
            {"id": 3, "name": "Priya Sharma", "port": 9003},
            {"id": 4, "name": "Vikram Patel", "port": 9004},
            {"id": 5, "name": "Sunita Reddy", "port": 9005},
        ]
        
        for driver in drivers:
            print(f"Starting Driver: {driver['name']} (Port {driver['port']})...")
            p = start_service_background(
                f"Driver {driver['name']}", driver['port'],
                [sys.executable, "-m", "uvicorn", "driver_instance.main:app", 
                 "--host", "0.0.0.0", "--port", str(driver['port'])],
                env_vars={
                    "DRIVER_ID": str(driver['id']),
                    "DRIVER_NAME": driver['name'],
                    "DRIVER_PORT": str(driver['port'])
                }
            )
            processes.append(p)
            time.sleep(1)
        
        print()
        print("=" * 60)
        print("All Services Started Successfully!")
        print("=" * 60)
        print()
        print("Access URLs:")
        print("  User Interface:     http://localhost:8000")
        print("  Backend API:        http://localhost:8001")
        print()
        print("Driver Dashboards:")
        print("  Rajesh Kumar:       http://localhost:9001")
        print("  Amit Singh:         http://localhost:9002")
        print("  Priya Sharma:       http://localhost:9003")
        print("  Vikram Patel:       http://localhost:9004")
        print("  Sunita Reddy:       http://localhost:9005")
        print()
        print("=" * 60)
        print("Press Ctrl+C to stop all services")
        print("=" * 60)
        print()
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping all services...")
        for process in processes:
            process.terminate()
        print("All services stopped.")
        
    except Exception as e:
        print(f"\nError: {e}")
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    main()
