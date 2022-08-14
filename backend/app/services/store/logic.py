from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.user.models import User
from app.services.store.models import Store


class StoreLogic:

    async def create_store(self, db: Session, name: str, user_id: int):
        user_query = select(User).where(User.id == user_id)
        user_res = await db.execute(user_query)
        user = user_res.scalars().first()

        store_obj = Store(
            user=user,
            name=name
        )
        db.add(store_obj)
        await db.commit()
        await db.refresh(store_obj)

        return True

    async def get_stores(self, db: Session, user_id: int):
        query = select(Store).where(Store.user_id == user_id)
        res = await db.execute(query)

        return [i.Store for i in res]
