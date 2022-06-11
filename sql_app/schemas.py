from typing import List, Union, Optional

from pydantic import BaseModel, Field


#Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

# Product
class ProductBase(BaseModel):
    name: str
    price: Optional[str] = Field(default="Without Price")
    price_sign: Optional[str] = Field(default="Without Price Sign")
    image_link: str
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


# Order
class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    product_ids: List[int]
    address: str


class OrderOut(OrderBase):
    id: int
    products: List[Product]
    address: str

class Order(OrderBase):
    id: int
    products: List[Product]

    owner_id: int

    class Config:
        orm_mode = True



# User
class UserBase(BaseModel):
    username: str
    name: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    orders: Optional[List[Order]]=[]
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    orders: List[Order]




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



