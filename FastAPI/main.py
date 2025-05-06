from fastapi import FastAPI, HTTPException, Depends, Request
from models import UserData, get_rozet
from scoring import calculate_score
from users import User, register_user, authenticate_user
from auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordRequestForm
from advice import get_gemini_advice
from gemini_api import get_gemini_response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils.predict import predict_sentiment
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="Frontend"), name="static")
templates = Jinja2Templates(directory="Frontend")

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

class InputText(BaseModel):
    text: str

@app.post("/predict")
async def predict(input_text: InputText):
    result = predict_sentiment(input_text.text)
    return {"prediction": result}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register_index.html", {"request": request})

@app.get("/calculate", response_class=HTMLResponse)
async def calculate_page(request: Request):
    return templates.TemplateResponse("calculate.html", {"request": request})

@app.get("/hero", response_class=HTMLResponse)
async def hero_page(request: Request):
    return templates.TemplateResponse("heropage_index.html", {"request": request})

@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@app.get("/badge", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("badge.html", {"request": request})
