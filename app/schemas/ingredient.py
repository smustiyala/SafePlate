from pydantic import BaseModel


class IngredientCreate(BaseModel):
    name: str
    is_vegan: bool = True
    is_vegetarian: bool = True
    contains_dairy: bool = False
    contains_egg: bool = False
    contains_nuts: bool = False


class IngredientResponse(BaseModel):
    id: int
    name: str
    is_vegan: bool
    is_vegetarian: bool
    contains_dairy: bool
    contains_egg: bool
    contains_nuts: bool

    class Config:
        from_attributes = True