from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.user.models import User
from app.services.store.models import Store
from app.services.products.models import Product, StoreProduct, ProductSupply, ProductRealization


class ProductLogic:

    async def create_product(self, db: Session, name: str, user_id: int):
        user_query = select(User).where(User.id == user_id)
        user_res = await db.execute(user_query)
        user = user_res.scalars().first()

        product_obj = Product(
            user=user,
            name=name
        )
        db.add(product_obj)
        await db.commit()
        await db.refresh(product_obj)

        return True

    async def get_products(self, db: Session, user_id: int):
        query = select(Product).where(Product.user_id == user_id)
        res = await db.execute(query)

        return [i.Product for i in res]

    async def create_store_product(self, db: Session, product_id: int, store_id: int):
        product_query = select(Product).where(Product.id == product_id)
        product_res = await db.execute(product_query)
        product = product_res.scalars().first()

        store_query = select(Store).where(Store.id == store_id)
        store_res = await db.execute(store_query)
        store = store_res.scalars().first()

        store_product_obj = StoreProduct(
            product=product,
            store=store
        )

        db.add(store_product_obj)
        await db.commit()
        await db.refresh(store_product_obj)
