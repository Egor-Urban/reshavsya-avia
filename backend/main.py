# backend/main.py



from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from .models import User
from .auth import hash_pw, verify_pw, make_token, current_user
from .forecast import load, all_routes, route_dates, calc



app = FastAPI()
Base.metadata.create_all(bind=engine)
load()



class RegBody(BaseModel):
    username: str
    password: str



class LoginBody(BaseModel):
    username: str
    password: str



class ForecastBody(BaseModel):
    route: str
    date: str
    price: float


# API
@app.post("/api/register")
def register(body: RegBody, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(400, "User already exist")
    
    db.add(User(username=body.username, password=hash_pw(body.password)))
    db.commit()
    
    return {"ok": True}


@app.post("/api/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    
    if not user or not verify_pw(body.password, user.password):
        raise HTTPException(401, "Invalid data")
    
    return {"token": make_token(body.username)}


@app.get("/api/routes")
def routes(_=Depends(current_user)):
    return all_routes()


@app.get("/api/dates/{route}")
def dates(route: str, _=Depends(current_user)):
    return route_dates(route)


@app.post("/api/forecast")
def forecast(body: ForecastBody, _=Depends(current_user)):
    result = calc(body.route, body.date, body.price)
    
    if not result:
        raise HTTPException(404, "Not found")
    
    return result



app.mount("/", StaticFiles(directory="frontend", html=True), name="static")