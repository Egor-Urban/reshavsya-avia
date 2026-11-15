# backend/auth.py



from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User


# NOT FOR PROD, ONLY TESTING
SECRET = "reshavsya_avia_secret"
ALGO = "HS256"
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")



def hash_pw(pw):
    return crypt.hash(pw)


def verify_pw(pw, hashed):
    return crypt.verify(pw, hashed)


def make_token(username):
    exp = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALGO)


def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=401)
        
        return user
    
    except Exception:
        raise HTTPException(status_code=401, detail="Not authorized")