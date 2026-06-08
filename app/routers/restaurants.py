from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse
from app.models.ingredient import Ingredient

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    existing_restaurant = db.query(Restaurant).filter(
        Restaurant.name == restaurant.name
    ).first()

    if existing_restaurant:
        raise HTTPException(
            status_code=400,
            detail="Restaurant already exists"
        )

    new_restaurant = Restaurant(
        name=restaurant.name,
        website=restaurant.website
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.post("/{restaurant_id}/menu-items", response_model=MenuItemResponse)
def create_menu_item(
    restaurant_id: int,
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    new_menu_item = MenuItem(
        name=menu_item.name,
        restaurant_id=restaurant_id
    )

    db.add(new_menu_item)
    db.commit()
    db.refresh(new_menu_item)

    return new_menu_item


@router.get("/{restaurant_id}/menu-items", response_model=List[MenuItemResponse])
def get_menu_items(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id
    ).all()

@router.post("/menu-items/{menu_item_id}/ingredients/{ingredient_id}")
def add_ingredient_to_menu_item(
    menu_item_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    menu_item = db.query(MenuItem).filter(
        MenuItem.id == menu_item_id
    ).first()

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    if ingredient in menu_item.ingredients:
        raise HTTPException(
            status_code=400,
            detail="Ingredient already added to this menu item"
        )

    menu_item.ingredients.append(ingredient)
    db.commit()

    return {
        "message": f"{ingredient.name} added to {menu_item.name}"
    }

@router.delete("/{restaurant_id}/menu-items/{menu_item_id}")
def delete_menu_item(
    restaurant_id: int,
    menu_item_id: int,
    db: Session = Depends(get_db)
):
    menu_item = db.query(MenuItem).filter(
        MenuItem.id == menu_item_id,
        MenuItem.restaurant_id == restaurant_id
    ).first()

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found for this restaurant"
        )

    db.delete(menu_item)
    db.commit()

    return {
        "message": "Menu item deleted"
    }

@router.put("/{restaurant_id}/menu-items/{menu_item_id}", response_model=MenuItemResponse)
def update_menu_item(
    restaurant_id: int,
    menu_item_id: int,
    menu_item_update: MenuItemCreate,
    db: Session = Depends(get_db)
):
    menu_item = db.query(MenuItem).filter(
        MenuItem.id == menu_item_id,
        MenuItem.restaurant_id == restaurant_id
    ).first()

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found for this restaurant"
        )

    menu_item.name = menu_item_update.name

    db.commit()
    db.refresh(menu_item)

    return menu_item