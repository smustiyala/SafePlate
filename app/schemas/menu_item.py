from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    name: str


class MenuItemResponse(BaseModel):
    id: int
    name: str
    restaurant_id: int

    class Config:
        from_attributes = True