from fastapi import APIRouter
from core.config import settings

router = APIRouter(prefix='/user', tags=['user'])


@router.get('')
async def test():
    return [settings.DATABASE_URL]
