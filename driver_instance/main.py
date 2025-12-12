from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import sys
from typing import List
from datetime import datetime

# Get driver info from environment variables (set by run script)
DRIVER_ID = int(os.getenv('DRIVER_ID', '1'))
DRIVER_NAME = os.getenv('DRIVER_NAME', 'Unknown Driver')
DRIVER_PORT = int(os.getenv('DRIVER_PORT', '9001'))

app = FastAPI(title=f"SwiftRide Driver - {DRIVER_NAME}")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Backend service URL
BACKEND_URL = "http://localhost:8001"

# In-memory storage for ride notifications
pending_rides = []
my_rides = []

@app.get("/", response_class=HTMLResponse)
async def driver_dashboard(request: Request):
    """Render driver dashboard"""
    return templates.TemplateResponse("driver_flash.html", {
        "request": request,
        "driver_id": DRIVER_ID,
        "driver_name": DRIVER_NAME,
        "driver_port": DRIVER_PORT
    })

@app.post("/api/new-ride-notification")
async def receive_ride_notification(ride_data: dict):
    """Receive broadcast notification of new ride from backend"""
    # Add to pending rides if not already there
    if not any(r['id'] == ride_data['id'] for r in pending_rides):
        pending_rides.append(ride_data)
    return {"status": "received"}

@app.get("/api/pending-rides")
async def get_pending_rides():
    """Get pending rides for this driver directly from backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/rides?status=PENDING")
            return response.json()
        except:
            return []

@app.get("/api/my-rides")
async def get_my_rides():
    """Get rides assigned to this driver"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/drivers/{DRIVER_ID}/rides")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return []

@app.post("/api/accept-ride/{ride_id}")
async def accept_ride(ride_id: int):
    """Accept a ride"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides/{ride_id}/accept",
                json={"driver_id": DRIVER_ID}
            )
            response.raise_for_status()
            
            # Remove from pending rides
            global pending_rides
            pending_rides = [r for r in pending_rides if r['id'] != ride_id]
            
            return response.json()
        except httpx.HTTPError as e:
            return JSONResponse(
                content={"error": "Failed to accept ride. It may have been taken by another driver."},
                status_code=400
            )

@app.post("/api/complete-ride/{ride_id}")
async def complete_ride(ride_id: int):
    """Complete a ride"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides/{ride_id}/complete",
                json={"driver_id": DRIVER_ID}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to complete ride"}, status_code=500)

@app.post("/api/reject-ride/{ride_id}")
async def reject_ride(ride_id: int):
    """Reject a ride"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides/{ride_id}/reject",
                json={"driver_id": DRIVER_ID}
            )
            response.raise_for_status()
            
            # Remove from pending rides
            global pending_rides
            pending_rides = [r for r in pending_rides if r['id'] != ride_id]
            
            return response.json()
        except httpx.HTTPError as e:
            return JSONResponse(
                content={"error": "Failed to reject ride"},
                status_code=400
            )

@app.get("/api/driver-info")
async def get_driver_info():
    """Get current driver information"""
    return {
        "id": DRIVER_ID,
        "name": DRIVER_NAME,
        "port": DRIVER_PORT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=DRIVER_PORT)
