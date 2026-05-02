from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name:str
    email: str
    password: str
    phone:str

class UserResponse(BaseModel):
    id: int
    name:str
    email: str
    phone: str

    class Config:
        from_attributes = True  
class RestaurantCreate(BaseModel):
    name: str
    location: str
    cuisine: str

class RestaurantResponse(BaseModel):
    id: int         
    name: str
    location: str
    cuisine: str
    owner_id: int

    class Config:
        from_attributes = True
class MenuItemCreate(BaseModel):
    name: str
    price: float
    category: str
    restaurant_id: int
class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    restaurant_id: int

    class Config:
        from_attributes = True
class OrderCreate(BaseModel):
    item_id: int
    quantity: int       

class OrderResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int
    status: str

    class Config:
        from_attributes = True