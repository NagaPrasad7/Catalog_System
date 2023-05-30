from pydantic import BaseModel


class Product(BaseModel):
    name: str
    category: str
    sku: str
    price: float
    quantity: int

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


# class Category(BaseModel):
#     name: str

#     class Config:
#         orm_mode = True
