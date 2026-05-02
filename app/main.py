from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db
import app.models as models
import app.schemas as schemas

app = FastAPI(
    title="Food Ordering API",
    description="A Swiggy-like food ordering backend",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Food Ordering API is running!"}
# GET all restaurants
@app.get("/restaurants", response_model=list[schemas.RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    return restaurants
@app.get("/restaurants/{restaurant_id}", response_model=schemas.RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
@app.delete("/restaurants/{restaurant_id}", response_model=schemas.RestaurantResponse)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(restaurant)
    db.commit()
    return {"message": f"Restaurant {restaurant_id} deleted successfully"}

# POST restaurant
@app.post("/restaurants", response_model=schemas.RestaurantResponse)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = models.Restaurant(
        name=restaurant.name,
        location=restaurant.location,
        cuisine=restaurant.cuisine,
        owner_id=1  # hardcoded for now, Week 5 JWT will fix this
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant
# GET menu items for a restaurant
@app.get("/restaurants/{restaurant_id}/menu", response_model=list[schemas.MenuItemResponse])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    # Check if restaurant exists
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Get all menu items for this restaurant
    menu_items = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()
    return menu_items

# POST add menu item to restaurant
@app.post("/restaurants/{restaurant_id}/menu", response_model=schemas.MenuItemResponse)
def add_menu_item(restaurant_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    # Check if restaurant exists
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    new_item = models.MenuItem(
        name=item.name,
        price=item.price,
        category=item.category,
        restaurant_id=restaurant_id  # from URL not body!
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
# POST order
@app.post("/orders", response_model=schemas.OrderResponse)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    
    # Step 1 - Check if menu item exists
    item = db.query(models.MenuItem).filter(models.MenuItem.id == order.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Step 2 - Create order
    new_order = models.Order(
        user_id=1,           # hardcoded for now, JWT will fix in Week 5
        item_id=order.item_id,
        quantity=order.quantity,
        status="pending"     # default status
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# GET all orders
@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders