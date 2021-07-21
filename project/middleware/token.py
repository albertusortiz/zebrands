import os

import jwt

from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from fastapi import status

from datetime import datetime
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv('SECRETKEYWORD')


oauth2_schema = OAuth2PasswordBearer(tokenUrl=' /api/v1/usuarios/login')


def create_token(username, nivel):
    data = {
        "nivel": nivel,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=5)
    }
    # Guardemos el access token en la BD
    # Generemos un refresh token
    return jwt.encode(data, SECRET, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        return None

def get_current_user(token: str = Depends(oauth2_schema)):
    data = decode_token(token)
    
    if data and data.get('nivel') and data.get('username') and data.get('exp'):
        if datetime.fromtimestamp(data['exp']) > datetime.utcnow():
            return data

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="El token no es valido.",
        headers={"WWW-Authenticate": "Bearer"}
    )