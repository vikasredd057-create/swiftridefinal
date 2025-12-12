from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EssentialsOrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class RideRequestCreate(BaseModel):
    source: str  # Format: "lat,lng"
    destination: str  # Format: "lat,lng"
    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    distance_km: Optional[float] = None
    essentials: Optional[List[EssentialsOrderItemCreate]] = []
    custom_essentials_request: Optional[str] = None

# --- Swift Essentials Schemas (Moved up for Forward Ref) ---

class PartnerStoreBase(BaseModel):
    name: str
    address: str
    lat: str
    lng: str
    contact_info: Optional[str] = None

class PartnerStoreCreate(PartnerStoreBase):
    pass

class PartnerStoreResponse(PartnerStoreBase):
    id: int
    class Config:
        from_attributes = True

class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryResponse(ProductCategoryBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    category_id: int
    store_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: int
    image_url: Optional[str] = None
    is_age_restricted: bool = False
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class EssentialsOrderItemResponse(BaseModel):
    id: int
    product_id: int
    product: Optional[ProductResponse] = None
    quantity: int
    price_at_booking: int
    class Config:
        from_attributes = True

class EssentialsOrderCreate(BaseModel):
    items: List[EssentialsOrderItemCreate]

class EssentialsOrderResponse(BaseModel):
    id: int
    ride_request_id: int
    total_amount: int
    status: str
    fulfillment_method: str
    pickup_store_id: Optional[int]
    custom_request: Optional[str] = None
    created_at: datetime
    items: List[EssentialsOrderItemResponse] = []
    class Config:
        from_attributes = True

class RideRequestResponse(BaseModel):
    id: int
    source: str
    destination: str
    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    distance_km: Optional[float] = None
    price: Optional[int] = None
    status: str
    driver_id: Optional[int] = None
    created_at: datetime
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    essentials_order: Optional[EssentialsOrderResponse] = None
    
    class Config:
        from_attributes = True

class DriverResponse(BaseModel):
    id: int
    name: str
    phone: str
    vehicle_number: str
    driver_port: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AcceptRideRequest(BaseModel):
    driver_id: int

class CompleteRideRequest(BaseModel):
    driver_id: int

class RejectRideRequest(BaseModel):
    driver_id: int

