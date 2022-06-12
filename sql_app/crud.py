import math

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from . import models, schemas, auth
from typing import List, Union, Optional
from datetime import datetime,timedelta
from jose import jwt, JWTError


# Order
def create_order(db: Session, user_id: int, product_ids: List[int], address: str):
    db_order = models.Order(owner_id=user_id, products=[], address=address)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for product_id in product_ids:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        db_order.products.append(db_product)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, user_id: int):
   return db.query(models.Order).filter(models.Order.owner_id == user_id).all()

# User
def get_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        return db_user


def register_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, username=user.username,  hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User(name=db_user.name, username=db_user.username, id=db_user.id, orders=[])



def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return f"User {user_id} was successfully deleted"
    else:
        return "User not found"
# JWT


SECRET_KEY = "43d040a66b3ca9bd85234d624a0786603712ce406f51e14a646b71b01c80de8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



#Brand
def get_brands(db: Session):
    return db.query(models.Brand).all()


def get_brand_by_name(db: Session, brand_name: str):
    return db.query(models.Brand).filter(models.Brand.name == brand_name).first()


def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

#Category
def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category_by_name(db: Session, category_name: str):
    return db.query(models.Category).filter(models.Category.name == category_name).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

#Product Type
def get_product_types(db: Session):
    return db.query(models.ProductType).all()


def get_product_type_by_name(db: Session, product_type_name: str):
    return db.query(models.ProductType).filter(models.ProductType.name == product_type_name).first()


def create_product_type(db: Session, product_type: schemas.ProductTypeCreate):
    db_product_type = models.ProductType(name=product_type.name)
    db.add(db_product_type)
    db.commit()
    db.refresh(db_product_type)
    return db_product_type


def add_category_to_product_type(db: Session, product_type_name: str, categories: List[schemas.CategoryCreate]):
    db_product_type = db.query(models.ProductType).filter(models.ProductType.name == product_type_name).first()
    for category in categories:
        db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
        if db_category:
            db_product_type.categories.append(db_category)
        else:
            db_category = create_category(db=db, category=category)
            db_product_type.categories.append(db_category)
        db.commit()
        db.refresh(db_product_type)
    return db_product_type

#Products
def get_products(
        db: Session,
        product_type: Optional[str] = None,
        category: Optional[str] = None,
        brand_name: Optional[str] = None,
        page: Optional[int] = None
        ):
    filters = []
    if product_type is None and category is None and brand_name is None:
        if page is not None:
            print(f"reauested page {page}")
            pages_count = db.query(models.Product).count()
            db_products = db.query(models.Product).offset((page-1) * 9).limit(9).all()
            db_products = schemas.ProductOut(products=db_products, page=page, pages_count=math.ceil(pages_count/9))
        else:
            db_products = db.query(models.Product).all()
            db_products = schemas.ProductOut(products=db_products, page=None, pages_count=None)
    else:
        if product_type:
            filters.append(f"product_type_name='{product_type}'")
        if category:
            filters.append(f"category_name='{category}'")
        if brand_name:
            filters.append(f"brand_name='{brand_name}'")
        filters = ' AND '.join(filters)
        print(page)
        if page is not None:
            print(f"reauested page {page}")
            pages_count = db.query(models.Product).filter(text(filters)).count()
            db_products = db.query(models.Product).filter(text(filters)).offset((page-1)*9).limit(9).all()
            db_products = schemas.ProductOut(products=db_products, page=page, pages_count=math.ceil(pages_count/9))
        else:
            db_products = db.query(models.Product).filter(text(filters)).all()
            db_products = schemas.ProductOut(products=db_products, page=None, pages_count=None)


    return db_products

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, products: List[schemas.ProductCreate]):
    new_products=[]
    for product in products:
        db_product_type = db.query(models.ProductType).filter(models.ProductType.name == product.product_type_name).first()
        if db_product_type is None:
            db_product_type = create_product_type(db=db, product_type=schemas.ProductTypeCreate(name=product.product_type_name))
        add_category_to_product_type(
            db=db,
            product_type_name=db_product_type.name,
            categories=[schemas.CategoryCreate(name=product.category_name)]
        )
        db_brand = db.query(models.Brand).filter(models.Brand.name == product.brand_name).first()
        if db_brand is None:
            create_brand(db=db, brand=schemas.BrandCreate(name=product.brand_name))
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        new_products.append(db_product)
    return new_products



