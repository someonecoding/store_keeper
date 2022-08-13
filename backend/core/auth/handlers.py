from fastapi import HTTPException
from fastapi.security import HTTPBearer

from core.config import settings
from passlib.context import CryptContext

import jwt
from datetime import datetime, timedelta


class AuthHandler:
    secret_key = settings.SECRET_KEY
    security = HTTPBearer()
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, hashed_password):
        return self.hasher.verify(password, hashed_password)

    def encode_token(self, id):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
        'scope': 'access_token',
            'sub' : id
        }
        return jwt.encode(
            payload, 
            self.secret_key,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']   
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, id):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, hours=10),
            'iat' : datetime.utcnow(),
        'scope': 'refresh_token',
            'sub' : id
        }
        return jwt.encode(
            payload, 
            self.secret_key,
            algorithm='HS256'
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=['HS256'])
            if (payload['scope'] == 'refresh_token'):
                id = payload['sub']
                new_token = self.encode_token(id)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')

