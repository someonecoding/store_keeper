import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime
import core.db.database as _database


class Store(_database.Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_created = Column(DateTime, default=dt.datetime.utcnow)
