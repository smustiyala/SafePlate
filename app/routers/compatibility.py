from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant

router = APIRouter(
    prefix="/compatibility",
    tags=["Compatibility"]
)


def analyze_ingredient(ingredient):
    compatible_with = []
    incompatible_with = []

    if ingredient.is_vegan:
        compatible_with.append("Vegan")
    else:
        incompatible_with.append("Vegan")

    if ingredient.is_vegetarian:
        compatible_with.append("Vegetarian")
    else:
        incompatible_with.append("Vegetarian")

    if not ingredient.contains_dairy:
        compatible_with.append("Dairy-Free")
    else:
        incompatible_with.append("Dairy-Free")

    if not ingredient.contains_egg:
        compatible_with.append("Egg-Free")
    else:
        incompatible_with.append("Egg-Free")

    if not ingredient.contains_nuts:
        compatible_with.append("Nut-Free")
    else:
        incompatible_with.append("Nut-Free")

    return {
        "ingredient": ingredient.name,
        "compatible_with": compatible_with,
        "incompatible_with": incompatible_with
    }


def evaluate_menu_item(menu_item, preference_names):
    issues = []
    recommendations = []
    ingredient_analysis = []

    for ingredient in menu_item.ingredients:
        ingredient_analysis.append(analyze_ingredient(ingredient))

        if "Vegan" in preference_names and not ingredient.is_vegan:
            issues.append(f"{ingredient.name} is not vegan")
            recommendations.append(f"Remove {ingredient.name}")

        if "Vegetarian" in preference_names and not ingredient.is_vegetarian:
            issues.append(f"{ingredient.name} is not vegetarian")
            recommendations.append(f"Remove {ingredient.name}")

        if "Dairy-Free" in preference_names and ingredient.contains_dairy:
            issues.append(f"{ingredient.name} contains dairy")
            recommendations.append(f"Remove {ingredient.name}")

        if "Egg-Free" in preference_names and ingredient.contains_egg:
            issues.append(f"{ingredient.name} contains egg")
            recommendations.append(f"Remove {ingredient.name}")

        if "Nut-Free" in preference_names and ingredient.contains_nuts:
            issues.append(f"{ingredient.name} contains nuts")
            recommendations.append(f"Remove {ingredient.name}")

    recommendations = list(dict.fromkeys(recommendations))

    if not issues:
        status = "safe"
    elif len(recommendations) < len(menu_item.ingredients):
        status = "modifiable"
    else:
        status = "unsafe"

    return {
        "menu_item": menu_item.name,
        "status": status,
        "issues": issues,
        "recommendations": recommendations,
        "ingredient_analysis": ingredient_analysis
    }


@router.get("/users/{user_id}/menu-items/{menu_item_id}")
def check_compatibility(
    user_id: int,
    menu_item_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    preference_names = {
        preference.name
        for preference in user.dietary_preferences
    }

    result = evaluate_menu_item(menu_item, preference_names)

    return {
        "user": user.username,
        **result
    }


@router.get("/restaurants/{restaurant_id}/compatible-menu-items/{user_id}")
def get_compatible_menu_items(
    restaurant_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    preference_names = {
        preference.name
        for preference in user.dietary_preferences
    }

    results = []

    for menu_item in restaurant.menu_items:
        results.append(
            evaluate_menu_item(menu_item, preference_names)
        )

    return {
        "restaurant": restaurant.name,
        "user": user.username,
        "results": results
    }