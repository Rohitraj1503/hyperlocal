from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserModel(BaseModel):
    id: Optional[UUID] = None
    role: str
    name: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True
    location: Optional[dict] = None
    model_config = ConfigDict(from_attributes=True)

class UserRegister(BaseModel):
    name: str
    role: str
    email: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    role: str

class InventoryModel(BaseModel):
    id: Optional[UUID] = None
    merchant_id: Optional[UUID] = None   # nullable — we use store_name for demo
    store_name: Optional[str] = None     # human-readable store identifier
    category: str
    type: Optional[str] = None
    name: str
    quantity: int = 0
    price: float
    model_config = ConfigDict(from_attributes=True)

class InventoryCreate(BaseModel):
    store_name: Optional[str] = None
    category: str
    type: Optional[str] = None
    name: str
    quantity: int = 0
    price: float

class OrderItemModel(BaseModel):
    id: Optional[UUID] = None
    inventory_id: Optional[UUID] = None
    name: Optional[str] = None
    quantity: int
    price_at_time: float
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    """Flexible order model for frontend — no UUID auth required"""
    customer_name: Optional[str] = None
    store_name: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    status: str = 'pending'
    total_amount: float
    items: Optional[List[dict]] = []

class OrderModel(BaseModel):
    id: Optional[str] = None
    customer_id: Optional[UUID] = None
    merchant_id: Optional[UUID] = None
    rider_id: Optional[UUID] = None
    customer_name: Optional[str] = None
    store_name: Optional[str] = None
    delivery_address: Optional[str] = None
    status: str = 'pending'
    total_amount: float
    pickup_location: Optional[dict] = None
    dropoff_location: Optional[dict] = None
    items: Optional[List[dict]] = []
    model_config = ConfigDict(from_attributes=True)
