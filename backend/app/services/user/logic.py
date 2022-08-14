from core.auth.handlers import AuthHandler

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate


class UserLogic:
    def __init__(self):
        self.auth_handler = AuthHandler()

    async def get_user_by_email(self, db: Session, email: str):
        query = select(User).where(User.email == email)
        res = await db.execute(query)
        return res.scalars().first()

    async def check_email(self, db: Session, email: str):
        if await self.get_user_by_email(db, email):
            return True
        return False

    async def create_user(self, db: Session, user: UserCreate):

        if await self.check_email(db=db, email=user.email):
            return False, 'User with same email already exists.'

        hashed_password = self.auth_handler.get_password_hash(user.password)
        user_obj = User(email=user.email, hashed_password=hashed_password)

        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)

        return True, user_obj
