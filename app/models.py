from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100))
    email    = Column(String(100), unique=True)
    password = Column(String(255))
    phone    = Column(String(15))

    # Relationships
    orders      = relationship("Order", back_populates="user")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100))
    location = Column(String(200))
    cuisine  = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    menu_items = relationship("MenuItem", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = "menu_items"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(100))
    price         = Column(Float)
    category      = Column(String(50))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    # Relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")

class Order(Base):
    __tablename__ = "orders"

    id       = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    item_id  = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)
    status   = Column(String(50), default="pending")

    # Relationships
    user = relationship("User", back_populates="orders")
    item = relationship("MenuItem")