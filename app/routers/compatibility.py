from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.models.menu_item import MenuItem

router = APIRouter(
    prefix="/compatibility",
    tags=["Compatibility"]
)

@router.get(
    "/users/{user_id}/menu-items/{menu_item_id}"
)
def check_compatibility(
    user_id: int,
    menu_item_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    menu_item = db.query(MenuItem).filter(
        MenuItem.id == menu_item_id
    ).first()

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    preference_names = {
        preference.name
        for preference in user.dietary_preferences
    }

    issues = []
    recommendations = []

    for ingredient in menu_item.ingredients:

        if (
            "Vegan" in preference_names
            and not ingredient.is_vegan
        ):
            issues.append(
                f"{ingredient.name} is not vegan"
            )

            recommendations.append(
                f"Remove {ingredient.name}"
            )

        if (
            "Dairy-Free" in preference_names
            and ingredient.contains_dairy
        ):
            issues.append(
                f"{ingredient.name} contains dairy"
            )

            recommendations.append(
                f"Remove {ingredient.name}"
            )

        if (
            "Egg-Free" in preference_names
            and ingredient.contains_egg
        ):
            issues.append(
                f"{ingredient.name} contains egg"
            )

            recommendations.append(
                f"Remove {ingredient.name}"
            )

        if (
            "Nut-Free" in preference_names
            and ingredient.contains_nuts
        ):
            issues.append(
                f"{ingredient.name} contains nuts"
            )

            recommendations.append(
                f"Remove {ingredient.name}"
            )

    if not issues:
        status = "safe"

    elif len(recommendations) < len(menu_item.ingredients):
        status = "modifiable"

    else:
        status = "unsafe"

    return {
        "user": user.username,
        "menu_item": menu_item.name,
        "status": status,
        "issues": issues,
        "recommendations": recommendations
    }