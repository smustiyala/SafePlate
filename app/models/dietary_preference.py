from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user_preference import user_preferences


class DietaryPreference(Base):
    __tablename__ = "dietary_preferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        secondary=user_preferences,
        back_populates="dietary_preferences"
    )