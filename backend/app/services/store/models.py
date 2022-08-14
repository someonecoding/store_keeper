import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import core.db.database as _database


class Store(_database.Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="stores")

    date_created = Column(DateTime, default=dt.datetime.utcnow)
