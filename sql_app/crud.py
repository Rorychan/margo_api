from sqlalchemy.orm import Session
from . import models, schemas

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

#Products
def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product