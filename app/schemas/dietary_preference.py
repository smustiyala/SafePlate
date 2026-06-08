from pydantic import BaseModel


class DietaryPreferenceCreate(BaseModel):
    name: str


class DietaryPreferenceResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True