from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from core.db.database import get_db
from core.auth.handlers import AuthHandler
from app.services.store import models, schemas
from app.services.store.logic import StoreLogic


router = APIRouter(prefix='/store', tags=['store'])
logic = StoreLogic()

auth = AuthHandler()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_store(store: schemas.StoreCreate, credentials: HTTPAuthorizationCredentials = Security(auth.security), db: Session = Depends(get_db)):
    token = credentials.credentials

    return await logic.create_store(
        user_id=auth.decode_token(token),
        name=store.name,
        db=db
    )


@router.get('')
async def get_stores(credentials: HTTPAuthorizationCredentials = Security(auth.security), db: Session = Depends(get_db)):
    token = credentials.credentials

    return await logic.get_stores(
        user_id=auth.decode_token(token),
        db=db
    )
