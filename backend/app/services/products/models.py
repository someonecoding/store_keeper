import datetime as dt

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
import core.db.database as _database


class Product(_database.Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="base_products")
    name = Column(String)


class StoreProduct(_database.Base):
    __tablename__ = "store_products"

    id = Column(Integer, primary_key=True, index=True)

    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store", backref="products")

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", backref="products")

    total_products = Column(Integer, default=0)
    avg_price = Column(Float, default=0)

    __table_args__ = (UniqueConstraint('store_id', 'product_id', name='_store_product_uc'),)


class AbstractProductTransaction(_database.Base):
    __abstract__ = True
    relation_name = 'transactions'

    @declared_attr
    def product_id(cls):
        return Column(Integer, ForeignKey("store_products.id"))

    @declared_attr
    def product(cls):
        return relationship("StoreProduct", backref=cls.relation_name)

    price = Column(Float)
    amount = Column(Integer)
    total_price = Column(Float)
    date_created = Column(DateTime, default=dt.datetime.utcnow)


class ProductSupply(AbstractProductTransaction):
    __tablename__ = 'product_supplies'
    relation_name = 'supplies'

    id = Column(Integer, primary_key=True, index=True)


class ProductRealization(AbstractProductTransaction):
    __tablename__ = 'product_realizations'
    relation_name = 'realizations'

    id = Column(Integer, primary_key=True, index=True)
