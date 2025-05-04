from pydantic import BaseModel
from typing import Dict
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db: Dict[str, str] = {} #Demo amaçlı bellek içi sahte veritabanı.

class User(BaseModel):
    username: str
    password: str


async def register_user(user: User) -> str:
    if user.username in fake_users_db:
        return "Kullanıcı zaten var."
    hashed = pwd_context.hash(user.password)
    fake_users_db[user.username] = hashed
    return "Kayıt başarılı."

async def authenticate_user(username: str, password: str) -> bool:
    hashed = fake_users_db.get(username)
    if not hashed:
        return False
    return pwd_context.verify(password, hashed)
