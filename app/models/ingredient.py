from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.menu_item_ingredient import menu_item_ingredients


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    is_vegan = Column(Boolean, default=True)
    is_vegetarian = Column(Boolean, default=True)
    contains_dairy = Column(Boolean, default=False)
    contains_egg = Column(Boolean, default=False)
    contains_nuts = Column(Boolean, default=False)

    menu_items = relationship(
        "MenuItem",
        secondary=menu_item_ingredients,
        back_populates="ingredients"
    )