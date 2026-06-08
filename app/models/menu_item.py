from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

from app.models.menu_item_ingredient import menu_item_ingredients


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )

    ingredients = relationship(
        "Ingredient",
        secondary=menu_item_ingredients,
        back_populates="menu_items"
    )