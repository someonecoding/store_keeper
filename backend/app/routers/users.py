from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from core.db.database import get_db
from core.validators import PasswordValidatorsGroup
from app.services.user import schemas, models
from app.services.user.logic import UserLogic

import email_validator


router = APIRouter(prefix='/user', tags=['user'])
logic = UserLogic()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        valid = email_validator.validate_email(email=user.email)
        email = valid.email
    except email_validator.EmailNotValidError:
        raise HTTPException(
            status_code=400, detail="Enter a valid email"
        )

    pwd_validation = PasswordValidatorsGroup.validate(user.password)
    if pwd_validation:
        raise HTTPException(
            status_code=400, detail=pwd_validation
        )

    success, message = await logic.create_user(db=db, user=user)

    if success:
        pass
    else:
        raise HTTPException(
            status_code=400, detail=message
        )

@router.post('/login')
async def login(user_details: schemas.UserCreate, db: Session = Depends(get_db)):
    user = await logic.get_user_by_email(email=user_details.email, db=db)
    if not user:
        return HTTPException(status_code=401, detail='Invalid email')
    if (not logic.auth_handler.verify_password(password=user_details.password, hashed_password=user.hashed_password)):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = logic.auth_handler.encode_token(user.id)
    refresh_token = logic.auth_handler.encode_refresh_token(user.id)
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(logic.auth_handler.security)):
    refresh_token = credentials.credentials
    new_token = logic.auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}
