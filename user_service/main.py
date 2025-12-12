from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os

app = FastAPI(title="SwiftRide User Service")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Backend service URL
BACKEND_URL = "http://localhost:8001"

# Get user info from environment variables
USER_ID = os.getenv('USER_ID', 'Guest')
USER_NAME = os.getenv('USER_NAME', 'Guest User')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render user homepage"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_id": USER_ID,
        "user_name": USER_NAME
    })

@app.post("/api/request-ride")
async def request_ride(ride_data: dict):
    """Submit a ride request to backend service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/rides",
                json=ride_data
            )
            response.raise_for_status()
            return JSONResponse(content=response.json(), status_code=200)
        except httpx.HTTPError as e:
            return JSONResponse(
                content={"error": "Failed to create ride request"},
                status_code=500
            )

@app.get("/api/essentials/products")
async def get_products():
    """Proxy request to backend service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/essentials/products")
            response.raise_for_status()
            return JSONResponse(content=response.json(), status_code=200)
        except httpx.HTTPError:
            return JSONResponse(content=[], status_code=200) # Return empty list on error

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
