from pydantic import BaseModel, Field

class UserData(BaseModel):
    car_km: float
    daily_water_use: float
    plastic_use: bool

    class Config:
        json_schema_extra = {
            'example': {
                'car_km': 15.0,
                'daily_water_use': 2,
                'plastic_use': False
            }
        }

def get_rozet(score: float) -> dict:
    if score < 50:
        return {"title": "Çevreye Zarar Veren", "emoji": "🥀"}
    elif score < 80:
        return {"title": "Yeşeren Yolcu", "emoji": "🌿"}
    else:
        return {"title": "Gezegen Koruyucusu", "emoji": "🌸"}
