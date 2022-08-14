from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from core.db.database import get_db
from core.auth.handlers import AuthHandler
from app.services.products import schemas
from app.services.products.logic import ProductLogic


router = APIRouter(prefix='/products', tags=['products'])
logic = ProductLogic()

auth = AuthHandler()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate, credentials: HTTPAuthorizationCredentials = Security(auth.security), db: Session = Depends(get_db)):
    token = credentials.credentials

    return await logic.create_product(
        user_id=auth.decode_token(token),
        name=product.name,
        db=db
    )


@router.get('')
async def get_products(credentials: HTTPAuthorizationCredentials = Security(auth.security), db: Session = Depends(get_db)):
    token = credentials.credentials

    return await logic.get_products(
        user_id=auth.decode_token(token),
        db=db
    )

@router.post('/store_product', status_code=status.HTTP_201_CREATED)
async def create_store_product(store_product: schemas.StoreProductCreate, credentials: HTTPAuthorizationCredentials = Security(auth.security), db: Session = Depends(get_db)):

    # owner perm

    return await logic.create_store_product(product_id=store_product.product_id, store_id=store_product.store_id, db=db)
