from fastapi import FastAPI, HTTPException, Depends
from models import UserData, get_rozet
from scoring import calculate_score
from users import User, register_user, authenticate_user
from auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordRequestForm
from advice import get_gemini_advice
from gemini_api import get_gemini_response


app = FastAPI()

@app.post("/calculate")
async def calculate_carbon_score(
    user_data: UserData,
    current_user: str = Depends(verify_token)
):
    print("Aktif Kullanıcı:", current_user)
    score = calculate_score(user_data.car_km, user_data.meat_days, user_data.plastic_use)
    rozet = get_rozet(score)

    return {
        "username": current_user,
        "carbon_score": score,
        "rozet": rozet
    }

@app.post("/register")
async def register(user: User):
    result = await register_user(user)
    if result == "Kullanıcı zaten var.":
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"message": result}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not await authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = await create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/gemini-advice")
async def generate_advice(user_data: UserData):
    try:
        score = calculate_score(user_data.car_km, user_data.daily_water_use, user_data.plastic_use)
        prompt_data = get_gemini_advice(user_data, score)
        prompt = prompt_data["prompt"]
        response = await get_gemini_response(prompt)
        return {"score": score, "advice": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#Burada bir /predict endpoint’i olacak. Kullanıcıdan metin alır, modeli çağırır, sonucu döner.

"""
from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.predict import predict_sentiment 

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/predict")
async def predict(input_text: InputText):
    result = predict_sentiment(input_text.text)
    return {"prediction": result}

"""