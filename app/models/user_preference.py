from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


user_preferences = Table(
    "user_preferences",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("preference_id", Integer, ForeignKey("dietary_preferences.id"), primary_key=True),
)