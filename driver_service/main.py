from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os

app = FastAPI(title="SwiftRide Driver Service")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Backend service URL
BACKEND_URL = "http://localhost:8001"

@app.get("/", response_class=HTMLResponse)
async def driver_dashboard(request: Request):
    """Render driver dashboard"""
    return templates.TemplateResponse("driver.html", {"request": request})

@app.get("/api/drivers")
async def get_drivers():
    """Get all drivers from backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/drivers")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to fetch drivers"}, status_code=500)

@app.get("/api/pending-rides")
async def get_pending_rides():
    """Get pending rides from backend"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/rides?status=PENDING")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to fetch rides"}, status_code=500)

@app.get("/api/driver/{driver_id}/rides")
async def get_driver_rides(driver_id: int):
    """Get rides for a specific driver"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/drivers/{driver_id}/rides")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to fetch driver rides"}, status_code=500)

@app.post("/api/accept-ride/{ride_id}")
async def accept_ride(ride_id: int, driver_id: int):
    """Accept a ride"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides/{ride_id}/accept",
                json={"driver_id": driver_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to accept ride"}, status_code=500)

@app.post("/api/complete-ride/{ride_id}")
async def complete_ride(ride_id: int, driver_id: int):
    """Complete a ride"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides/{ride_id}/complete",
                json={"driver_id": driver_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return JSONResponse(content={"error": "Failed to complete ride"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
