from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Brand
@app.get("/brands/", response_model=List[schemas.Brand], tags=["Brands"])
def read_brands(db: Session = Depends(get_db)):
    brands = crud.get_brands(db=db)
    return brands


@app.get("/brands/{brand_name}/", response_model=schemas.Brand, tags=["Brands"])
def read_brand(brand_name: str, db: Session = Depends(get_db)):
    return crud.get_brand_by_name(db=db, brand_name=brand_name)


@app.post("/brands/", response_model=schemas.Brand, tags=["Brands"])
def write_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = crud.get_brand_by_name(brand_name=brand.name, db=db)
    if db_brand:
        raise HTTPException(status_code=400, detail="Brand already exists")
    return crud.create_brand(brand=brand, db=db)

# Category
@app.get("/categories/", response_model=List[schemas.Category], tags=["Categories"])
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db=db)
    return categories


@app.get("/categories/{category_name}/", response_model=schemas.Category, tags=["Categories"])
def read_category(category_name: str, db: Session = Depends(get_db)):
    return crud.get_category_by_name(db=db, category_name=category_name)


@app.post("/categories/", response_model=schemas.Category, tags=["Categories"])
def write_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(category_name=category.name, db=db)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(category=category, db=db)


# Product type
@app.get("/product_types/", response_model=List[schemas.ProductType], tags=["Product Types"])
def read_product_types(db: Session = Depends(get_db)):
    product_types = crud.get_product_types(db=db)
    return product_types


@app.get("/product_types/{product_type_name}/", response_model=schemas.ProductType, tags=["Product Types"])
def read_product_type(product_type_name: str, db: Session = Depends(get_db)):
    return crud.get_product_type_by_name(db=db, product_type_name=product_type_name)


@app.post("/product_types/", response_model=schemas.ProductType, tags=["Product Types"])
def write_product_type(product_type: schemas.ProductTypeCreate, db: Session = Depends(get_db)):
    db_product_type = crud.get_product_type_by_name(product_type_name=product_type.name, db=db)
    if db_product_type:
        raise HTTPException(status_code=400, detail="Product type already exists")
    return crud.create_product_type(product_type=product_type, db=db)

# Products
@app.get("/products",response_model=schemas.Product, tags=["Products"])
def read_product(db: Session = Depends(get_db)):
    return crud.get_products(db=db)


@app.get("/products/{product_id}/", response_model=schemas.Product, tags=["Products"])
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_id(product_id=product_id, db=db)


@app.post(
    "/products",
    response_model=schemas.Product,
    tags=["Products"],
    response_description="Возвращает созданный продукт"
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    '''
    Добавляет продукт

    Если для продукта еще не созданы **Категория**, **Бренд**, или **Тип** они будут созданы **Автоматически**

    - **name**: Каждый продукт имеет свое уникальное имя
    - **description**: (Опционально) Описание продукта
    - **price**: Цена продукта
    - **product_type_name**: Тип продукта. Наппример **Eyeliner**
    - **brand_name**: Имя бренда. Например **Maybeline**
    - **category_name**: Категория товара. Например **Powder**
    '''
    if crud.get_product_type_by_name(db=db, product_type_name=product.product_type_name) is None:
        crud.create_product_type(db=db, product_type=schemas.ProductTypeCreate(name=product.product_type_name))
    if crud.get_category_by_name(db=db, category_name=product.category_name) is None:
        crud.create_category(db=db, category=schemas.CategoryCreate(name=product.category_name))
    if crud.get_brand_by_name(db=db, brand_name=product.brand_name) is None:
        crud.create_brand(db=db, brand=schemas.BrandCreate(name=product.brand_name))
    return crud.create_product(db=db, product=product)


