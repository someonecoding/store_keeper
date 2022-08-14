import pydantic


class StoreCreate(pydantic.BaseModel):
    name: str
