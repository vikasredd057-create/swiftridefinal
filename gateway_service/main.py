from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import subprocess
import sys
import os
import time
import socket
from typing import List, Dict

# Ensure we can import from backend_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend_service.database import SessionLocal
    from backend_service.models import Driver
except ImportError as e:
    print(f"Warning: Could not import backend_service models: {e}")
    SessionLocal = None
    Driver = None

app = FastAPI(title="SwiftRide Gateway")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# State
active_processes: List[subprocess.Popen] = []
user_ports = list(range(6000, 6021))
driver_ports = list(range(8000, 8021))
used_ports: Dict[int, str] = {} # port -> type ('user' or 'driver')

next_user_id = 1
# Driver ID is managed by DB

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_next_free_port(ports_list: List[int]) -> int:
    for port in ports_list:
        if port not in used_ports and not is_port_in_use(port):
            return port
    return None

def start_service_process(name, port, command, env_vars=None):
    """Start a service in the background"""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    # Platform specific flags
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        creationflags=creation_flags
    )
    return process

def create_driver_in_db(port: int, id_suffix: int):
    if not SessionLocal or not Driver:
        print("DB Not available, skipping DB creation for driver (Backend might fail to broadcast)")
        return id_suffix # Fallback
        
    db = SessionLocal()
    try:
        # Check if port exists
        existing = db.query(Driver).filter(Driver.driver_port == port).first()
        if existing:
            # If it exists, we might want to release it or reuse it
            # For now, let's reuse it or just update it
            existing.status = "AVAILABLE"
            existing.name = f"Driver {id_suffix}"
            db.commit()
            db.refresh(existing)
            return existing.id
            
        new_driver = Driver(
            name=f"Driver {id_suffix}",
            phone=f"9876543{id_suffix:03d}", # Dummy phone
            vehicle_number=f"DL-01-GW-{id_suffix:04d}",
            driver_port=port,
            status="AVAILABLE"
        )
        db.add(new_driver)
        db.commit()
        db.refresh(new_driver)
        return new_driver.id
    except Exception as e:
        print(f"Error creating driver in DB: {e}")
        db.rollback()
        return id_suffix # Fallback ID
    finally:
        db.close()

@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down child processes...")
    for p in active_processes:
        try:
            p.terminate()
        except:
            pass

@app.get("/", response_class=HTMLResponse)
async def gateway_dashboard(request: Request):
    is_backend_up = is_port_in_use(8001)
    status_color = "#00ff00" if is_backend_up else "#ff0000"
    
    return templates.TemplateResponse("gateway.html", {
        "request": request,
        "used_ports": used_ports,
        "backend_status": "Running" if is_backend_up else "Stopped"
    })

@app.get("/spawn/user")
async def spawn_user():
    global next_user_id
    port = get_next_free_port(user_ports)
    if not port:
        raise HTTPException(status_code=503, detail="No available ports for users (6000-6020)")
    
    user_id = next_user_id
    user_name = f"User {user_id}"
    next_user_id += 1
    
    # Command to run user service
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "user_service.main:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    
    env = {
        "USER_ID": str(user_id),
        "USER_NAME": user_name
    }
    
    try:
        proc = start_service_process(f"User {user_id}", port, cmd, env)
        active_processes.append(proc)
        used_ports[port] = f"User {user_id}"
        
        # Wait a bit for it to start
        time.sleep(1.5)
        
        return RedirectResponse(url=f"http://localhost:{port}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start user service: {e}")

@app.get("/spawn/driver")
async def spawn_driver():
    port = get_next_free_port(driver_ports)
    if not port:
        raise HTTPException(status_code=503, detail="No available ports for drivers (8000-8020)")
    
    # Generate a temporary ID based on port to ensure uniqueness in naming
    temp_suffix = port # Use port as suffix for uniqueness
    
    # Register in DB
    driver_id = create_driver_in_db(port, temp_suffix)
    driver_name = f"Driver {driver_id} (Port {port})"
    
    # Command to run driver instance
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "driver_instance.main:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    
    env = {
        "DRIVER_ID": str(driver_id),
        "DRIVER_NAME": driver_name,
        "DRIVER_PORT": str(port)
    }
    
    try:
        proc = start_service_process(f"Driver {driver_id}", port, cmd, env)
        active_processes.append(proc)
        used_ports[port] = f"Driver {driver_id}"
        
        # Wait a bit
        time.sleep(1.5)
        
        return RedirectResponse(url=f"http://localhost:{port}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start driver service: {e}")

@app.get("/admin")
async def admin_redirect():
    return RedirectResponse(url="/")
