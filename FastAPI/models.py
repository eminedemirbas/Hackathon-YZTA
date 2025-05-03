from pydantic import BaseModel, Field

class UserData(BaseModel):
    car_km: float = Field(..., gt=0)
    meat_days: int = Field(..., ge=0, le=7)
    plastic_use: bool = Field(...)
