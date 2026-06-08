from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    website: str | None = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    website: str | None = None

    class Config:
        from_attributes = True