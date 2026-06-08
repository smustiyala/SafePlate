from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem

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

