import pydantic


class ProductCreate(pydantic.BaseModel):
    name: str


class StoreProductCreate(pydantic.BaseModel):
    product_id: int
    store_id: int
