import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import core.db.database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, default=dt.datetime.utcnow)

    store = relationship("Store", backref="owner")
