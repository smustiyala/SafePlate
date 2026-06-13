from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.ingredient import Ingredient
from app.models.menu_item_ingredient import menu_item_ingredients
from app.models.dietary_preference import DietaryPreference
from app.models.user_preference import user_preferences
from app.seed_data import seed_database

from app.routers import compatibility
from app.routers import dietary_preferences
from app.routers import ingredients
from app.routers import restaurants
from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafePlate API",
    
    description="Dietary compatibility platform for restaurant menus.",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(ingredients.router)
app.include_router(dietary_preferences.router)
app.include_router(compatibility.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SafePlate API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/admin/seed")
def seed_database_endpoint():
    seed_database()
    return {
        "message": "Database seeded successfully"
    }