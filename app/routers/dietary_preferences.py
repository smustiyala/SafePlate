from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dietary_preference import DietaryPreference
from app.models.user import User
from app.schemas.dietary_preference import (
    DietaryPreferenceCreate,
    DietaryPreferenceResponse,
)

router = APIRouter(
    prefix="/dietary-preferences",
    tags=["Dietary Preferences"]
)


@router.post("/", response_model=DietaryPreferenceResponse)
def create_dietary_preference(
    preference: DietaryPreferenceCreate,
    db: Session = Depends(get_db)
):
    existing_preference = db.query(DietaryPreference).filter(
        DietaryPreference.name == preference.name
    ).first()

    if existing_preference:
        raise HTTPException(
            status_code=400,
            detail="Dietary preference already exists"
        )

    new_preference = DietaryPreference(name=preference.name)

    db.add(new_preference)
    db.commit()
    db.refresh(new_preference)

    return new_preference


@router.get("/", response_model=List[DietaryPreferenceResponse])
def get_dietary_preferences(db: Session = Depends(get_db)):
    return db.query(DietaryPreference).all()


@router.post("/users/{user_id}/preferences/{preference_id}")
def add_preference_to_user(
    user_id: int,
    preference_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    preference = db.query(DietaryPreference).filter(
        DietaryPreference.id == preference_id
    ).first()

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="Dietary preference not found"
        )

    if preference in user.dietary_preferences:
        raise HTTPException(
            status_code=400,
            detail="Preference already added to this user"
        )

    user.dietary_preferences.append(preference)
    db.commit()

    return {
        "message": f"{preference.name} added to {user.username}"
    }