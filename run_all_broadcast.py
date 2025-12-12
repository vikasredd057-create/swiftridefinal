"""
Script to run all services with individual driver instances.
Each driver runs on their own port and receives broadcast notifications.
"""
import subprocess
import sys
import time
import os

def run_services():
    print("Starting SwiftRide Microservices with Broadcast Architecture...")
    print("=" * 70)
    
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
    ]
    
    # Individual driver instances
    drivers = [
        {"id": 1, "name": "Rajesh Kumar", "port": 9001},
        {"id": 2, "name": "Amit Singh", "port": 9002},
        {"id": 3, "name": "Priya Sharma", "port": 9003},
        {"id": 4, "name": "Vikram Patel", "port": 9004},
        {"id": 5, "name": "Sunita Reddy", "port": 9005},
    ]
    
    for driver in drivers:
        services.append({
            "name": f"Driver {driver['name']}",
            "command": [
                sys.executable, "-m", "uvicorn", 
                "driver_instance.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(driver['port'])
            ],
            "port": driver['port'],
            "env": {
                "DRIVER_ID": str(driver['id']),
                "DRIVER_NAME": driver['name'],
                "DRIVER_PORT": str(driver['port'])
            }
        })
    
    processes = []
    
    try:
        for service in services:
            print(f"\nStarting {service['name']} on port {service['port']}...")
            
            # Prepare environment variables
            env = os.environ.copy()
            if 'env' in service:
                env.update(service['env'])
            
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            processes.append(process)
            time.sleep(1.5)  # Wait between starting services
        
        print("\n" + "=" * 70)
        print("All services started successfully!")
        print("\nService URLs:")
        print("   User Service:     http://localhost:8000")
        print("   Backend Service:  http://localhost:8001")
        print("\nDriver Dashboards:")
        print("   Rajesh Kumar:     http://localhost:9001")
        print("   Amit Singh:       http://localhost:9002")
        print("   Priya Sharma:     http://localhost:9003")
        print("   Vikram Patel:     http://localhost:9004")
        print("   Sunita Reddy:     http://localhost:9005")
        print("\nPress Ctrl+C to stop all services")
        print("=" * 70)
        
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
