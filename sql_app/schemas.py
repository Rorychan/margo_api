from typing import List, Union, Optional

from pydantic import BaseModel


#Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# User
class UserBase(BaseModel):
    username: str
    name: str
    address: Optional[str] = ""


class UserCreate(UserBase):
    password: str





class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int





# Product
class ProductBase(BaseModel):
    name: str
    price: str
    description: Optional[str] = ""
    product_type_name: str
    brand_name: str
    category_name: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# # Order
# class OrderBase(BaseModel):
#     user_id: int
#
#
#
# class OrderCreate(OrderBase):
#     pass
#
#
# class Order(OrderBase):
#     id: int
#     products: List[Product] = []
#     class Config:
#         orm_mode = True





# Brand
class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int
    class Config:
        orm_mode = True

# Category
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int


    class Config:
        orm_mode = True


# Product Type
class ProductTypeBase(BaseModel):
    name: str


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductType(ProductTypeBase):
    id: int
    categories: List[Category]
    class Config:
        orm_mode = True



