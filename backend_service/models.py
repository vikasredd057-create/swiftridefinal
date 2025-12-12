from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from datetime import datetime
import enum
from .database import Base

from sqlalchemy.orm import relationship

class RideStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    vehicle_number = Column(String, nullable=False)
    driver_port = Column(Integer, nullable=False, unique=True)  # Each driver has their own port
    status = Column(String, default="AVAILABLE")  # AVAILABLE, BUSY
    created_at = Column(DateTime, default=datetime.utcnow)

class RideRequest(Base):
    __tablename__ = "ride_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # Format: "lat,lng"
    destination = Column(String, nullable=False)  # Format: "lat,lng"
    source_address = Column(String, nullable=True)  # Human-readable address
    destination_address = Column(String, nullable=True)  # Human-readable address
    distance_km = Column(Integer, nullable=True)  # Distance in kilometers
    price = Column(Integer, nullable=True)  # Price in rupees
    status = Column(Enum(RideStatus), default=RideStatus.PENDING)
    driver_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    essentials_order = relationship("EssentialsOrder", back_populates="ride_request", uselist=False)

class PartnerStore(Base):
    __tablename__ = "partner_stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)

class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("partner_stores.id"), nullable=True) # If null, it's a driver-carry item
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False) # In smallest currency unit
    image_url = Column(String, nullable=True)
    is_age_restricted = Column(Boolean, default=False)
    stock_quantity = Column(Integer, default=0) # For simple inventory tracking

class EssentialsOrder(Base):
    __tablename__ = "essentials_orders"
    id = Column(Integer, primary_key=True, index=True)
    ride_request_id = Column(Integer, ForeignKey("ride_requests.id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(String, default="PENDING") # PENDING, PICKED_UP, DELIVERED, CANCELLED
    fulfillment_method = Column(String, nullable=False) # DRIVER_CARRY, DRIVER_PICKUP
    pickup_store_id = Column(Integer, ForeignKey("partner_stores.id"), nullable=True) # If pickup
    custom_request = Column(String, nullable=True) # User's manual request
    created_at = Column(DateTime, default=datetime.utcnow)

    ride_request = relationship("RideRequest", back_populates="essentials_order")
    items = relationship("EssentialsOrderItem", back_populates="order")
    store = relationship("PartnerStore")

class EssentialsOrderItem(Base):
    __tablename__ = "essentials_order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("essentials_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_booking = Column(Integer, nullable=False)

    order = relationship("EssentialsOrder", back_populates="items")
    product = relationship("Product")
