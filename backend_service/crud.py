from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def create_ride_request(db: Session, ride: schemas.RideRequestCreate):
    """Create a new ride request with automatic price calculation and essentials processing"""
    # Calculate price: ₹50 base fare + ₹15 per km
    distance = ride.distance_km or 0
    base_fare = 50
    per_km_rate = 15
    calculated_price = base_fare + (distance * per_km_rate)
    # Round to nearest ₹10
    final_price = round(calculated_price / 10) * 10
    
    db_ride = models.RideRequest(
        source=ride.source,
        destination=ride.destination,
        source_address=ride.source_address,
        destination_address=ride.destination_address,
        distance_km=int(distance) if distance else None,
        price=int(final_price),
        status=models.RideStatus.PENDING
    )
    db.add(db_ride)
    db.flush() # Flush to get ID

    # Handle Essentials
    if ride.essentials or ride.custom_essentials_request:
        essentials_total = 0
        order_items = []
        is_pickup = False
        pickup_store_id = None
        
        # Validate items and calculate total
        if ride.essentials:
            for item in ride.essentials:
                product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
                if product:
                    item_total = product.price * item.quantity
                    essentials_total += item_total
                    
                    # Check fulfillment type
                    if product.store_id:
                        is_pickup = True
                        if pickup_store_id is None:
                            pickup_store_id = product.store_id
                    
                    order_items.append({
                        "product": product,
                        "quantity": item.quantity,
                        "price": product.price
                    })
        
        if order_items or ride.custom_essentials_request:
            fulfillment_method = "DRIVER_PICKUP" if is_pickup else "DRIVER_CARRY"
            
            if ride.custom_essentials_request and not is_pickup:
                fulfillment_method = "DRIVER_PICKUP"

            db_order = models.EssentialsOrder(
                ride_request_id=db_ride.id,
                total_amount=essentials_total,
                status="PENDING",
                fulfillment_method=fulfillment_method,
                pickup_store_id=pickup_store_id,
                custom_request=ride.custom_essentials_request
            )
            db.add(db_order)
            db.flush()
            
            for item in order_items:
                db_item = models.EssentialsOrderItem(
                    order_id=db_order.id,
                    product_id=item["product"].id,
                    quantity=item["quantity"],
                    price_at_booking=item["price"]
                )
                db.add(db_item)

    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_products(db: Session, category_id: int = None):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.all()

def get_categories(db: Session):
    return db.query(models.ProductCategory).all()

def get_stores(db: Session):
    return db.query(models.PartnerStore).all()

def get_rides_by_status(db: Session, status: str):
    """Get all rides with a specific status"""
    return db.query(models.RideRequest).filter(
        models.RideRequest.status == status
    ).order_by(models.RideRequest.created_at).all()

def get_ride_by_id(db: Session, ride_id: int):
    """Get a specific ride by ID"""
    return db.query(models.RideRequest).filter(
        models.RideRequest.id == ride_id
    ).first()

def accept_ride(db: Session, ride_id: int, driver_id: int):
    """Accept a ride (atomic operation to prevent double-booking)"""
    ride = db.query(models.RideRequest).filter(
        models.RideRequest.id == ride_id,
        models.RideRequest.status == models.RideStatus.PENDING
    ).first()
    
    if not ride:
        return None
    
    # Update ride
    ride.status = models.RideStatus.ACCEPTED
    ride.driver_id = driver_id
    ride.accepted_at = datetime.utcnow()
    
    # Update driver status
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        driver.status = "BUSY"
    
    db.commit()
    db.refresh(ride)
    return ride

def complete_ride(db: Session, ride_id: int, driver_id: int):
    """Complete a ride"""
    ride = db.query(models.RideRequest).filter(
        models.RideRequest.id == ride_id,
        models.RideRequest.driver_id == driver_id,
        models.RideRequest.status == models.RideStatus.ACCEPTED
    ).first()
    
    if not ride:
        return None
    
    # Update ride
    ride.status = models.RideStatus.COMPLETED
    ride.completed_at = datetime.utcnow()
    
    # Update driver status
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        driver.status = "AVAILABLE"
    
    db.commit()
    db.refresh(ride)
    return ride

def get_driver_rides(db: Session, driver_id: int):
    """Get all rides for a specific driver"""
    return db.query(models.RideRequest).filter(
        models.RideRequest.driver_id == driver_id
    ).order_by(models.RideRequest.created_at.desc()).all()

def get_all_drivers(db: Session):
    """Get all drivers"""
    return db.query(models.Driver).all()

def get_driver_by_id(db: Session, driver_id: int):
    """Get a specific driver by ID"""
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()

def reject_ride(db: Session, ride_id: int, driver_id: int):
    """Reject a ride - this just marks that the driver declined it locally"""
    # For now, we just return success - the driver's frontend will remove it from their pending list
    # The ride remains PENDING for other drivers to accept
    ride = db.query(models.RideRequest).filter(
        models.RideRequest.id == ride_id,
        models.RideRequest.status == models.RideStatus.PENDING
    ).first()
    
    return ride  # Return the ride to confirm it exists and is still pending
