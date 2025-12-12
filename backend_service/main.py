from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import httpx
import asyncio
from . import crud, models, schemas
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwiftRide Backend Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def broadcast_ride_to_drivers(ride_data: dict, db: Session):
    """Broadcast new ride to all available drivers"""
    drivers = crud.get_all_drivers(db)
    
    async with httpx.AsyncClient(timeout=2.0) as client:
        tasks = []
        for driver in drivers:
            if driver.status == "AVAILABLE":
                try:
                    url = f"http://localhost:{driver.driver_port}/api/new-ride-notification"
                    tasks.append(client.post(url, json=ride_data))
                except Exception as e:
                    print(f"Failed to notify driver {driver.id}: {e}")
        
        # Send all notifications concurrently
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

@app.get("/")
def read_root():
    return {"service": "SwiftRide Backend Service", "status": "running"}

@app.post("/api/rides", response_model=schemas.RideRequestResponse)
async def create_ride(
    ride: schemas.RideRequestCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new ride request and broadcast to all drivers"""
    new_ride = crud.create_ride_request(db, ride)
    
    # Broadcast to all drivers in background
    ride_data = {
        "id": new_ride.id,
        "source": new_ride.source,
        "destination": new_ride.destination,
        "source_address": new_ride.source_address,
        "destination_address": new_ride.destination_address,
        "distance_km": new_ride.distance_km,
        "price": new_ride.price,
        "status": new_ride.status,
        "created_at": new_ride.created_at.isoformat(),
        "essentials": None
    }

    if new_ride.essentials_order:
        items = []
        for item in new_ride.essentials_order.items:
            items.append({
                "name": item.product.name,
                "quantity": item.quantity,
                "type": "PICKUP" if item.product.store_id else "CARRY"
            })
        
        ride_data["essentials"] = {
            "total_amount": new_ride.essentials_order.total_amount,
            "fulfillment": new_ride.essentials_order.fulfillment_method,
            "pickup_store": new_ride.essentials_order.store.name if new_ride.essentials_order.store else None,
            "pickup_address": new_ride.essentials_order.store.address if new_ride.essentials_order.store else None,
            "items": items,
            "custom_request": new_ride.essentials_order.custom_request
        }
    
    # Use background task to avoid blocking
    background_tasks.add_task(broadcast_ride_to_drivers, ride_data, db)
    
    return new_ride

@app.get("/api/rides", response_model=List[schemas.RideRequestResponse])
def get_rides(status: str = "PENDING", db: Session = Depends(get_db)):
    """Get rides by status"""
    return crud.get_rides_by_status(db, status)

@app.get("/api/rides/{ride_id}", response_model=schemas.RideRequestResponse)
def get_ride(ride_id: int, db: Session = Depends(get_db)):
    """Get a specific ride"""
    ride = crud.get_ride_by_id(db, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@app.post("/api/rides/{ride_id}/accept", response_model=schemas.RideRequestResponse)
def accept_ride(ride_id: int, request: schemas.AcceptRideRequest, db: Session = Depends(get_db)):
    """Accept a ride"""
    ride = crud.accept_ride(db, ride_id, request.driver_id)
    if not ride:
        raise HTTPException(status_code=400, detail="Ride not available or already accepted")
    return ride

@app.post("/api/rides/{ride_id}/complete", response_model=schemas.RideRequestResponse)
def complete_ride(ride_id: int, request: schemas.CompleteRideRequest, db: Session = Depends(get_db)):
    """Complete a ride"""
    ride = crud.complete_ride(db, ride_id, request.driver_id)
    if not ride:
        raise HTTPException(status_code=400, detail="Ride not found or cannot be completed")
    return ride

@app.get("/api/drivers", response_model=List[schemas.DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    """Get all drivers"""
    return crud.get_all_drivers(db)

@app.get("/api/drivers/{driver_id}", response_model=schemas.DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    """Get a specific driver"""
    driver = crud.get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@app.get("/api/drivers/{driver_id}/rides", response_model=List[schemas.RideRequestResponse])
def get_driver_rides(driver_id: int, db: Session = Depends(get_db)):
    """Get all rides for a driver"""
    return crud.get_driver_rides(db, driver_id)

@app.post("/api/rides/{ride_id}/reject", response_model=schemas.RideRequestResponse)
def reject_ride(ride_id: int, request: schemas.RejectRideRequest, db: Session = Depends(get_db)):
    """Reject a ride - driver declines without affecting other drivers"""
    ride = crud.reject_ride(db, ride_id, request.driver_id)
    if not ride:
        raise HTTPException(status_code=400, detail="Ride not found or already accepted")
    return ride

# --- Swift Essentials Endpoints ---

@app.get("/api/essentials/products", response_model=List[schemas.ProductResponse])
def get_products(category_id: int = None, db: Session = Depends(get_db)):
    return crud.get_products(db, category_id)

@app.post("/api/essentials/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/essentials/categories", response_model=List[schemas.ProductCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/api/essentials/categories", response_model=schemas.ProductCategoryResponse)
def create_category(category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    db_category = models.ProductCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/api/essentials/stores", response_model=List[schemas.PartnerStoreResponse])
def get_stores(db: Session = Depends(get_db)):
    return crud.get_stores(db)

@app.post("/api/essentials/stores", response_model=schemas.PartnerStoreResponse)
def create_store(store: schemas.PartnerStoreCreate, db: Session = Depends(get_db)):
    db_store = models.PartnerStore(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
