import datetime as dt
import pydantic


class UserBase(pydantic.BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    date_created: dt.datetime

    class Config:
        orm_mode = True
