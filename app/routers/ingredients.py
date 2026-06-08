from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientResponse

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


@router.post("/", response_model=IngredientResponse)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db)
):
    existing_ingredient = db.query(Ingredient).filter(
        Ingredient.name == ingredient.name
    ).first()

    if existing_ingredient:
        raise HTTPException(
            status_code=400,
            detail="Ingredient already exists"
        )

    new_ingredient = Ingredient(**ingredient.model_dump())

    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient


@router.get("/", response_model=List[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()