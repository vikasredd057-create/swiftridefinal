"""
Test script to start a single driver instance
"""
import os
import subprocess
import sys

# Set environment variables for driver 1
os.environ['DRIVER_ID'] = '1'
os.environ['DRIVER_NAME'] = 'Rajesh Kumar'
os.environ['DRIVER_PORT'] = '9001'

# Start the driver instance
print("Starting Rajesh Kumar on port 9001...")
print(f"Environment: DRIVER_ID={os.environ['DRIVER_ID']}, DRIVER_NAME={os.environ['DRIVER_NAME']}, DRIVER_PORT={os.environ['DRIVER_PORT']}")

subprocess.run([
    sys.executable, "-m", "uvicorn",
    "driver_instance.main:app",
    "--host", "0.0.0.0",
    "--port", "9001"
])
