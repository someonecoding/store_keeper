from fastapi import APIRouter


router = APIRouter(prefix='/user', tags=['user'])


@router.get('')
async def test():
    return {"message": "test"}
