from typing import List,Union
from datetime import datetime,timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import SessionLocal, engine
from jose import JWTError, jwt



models.Base.metadata.create_all(bind=engine)


SECRET_KEY = "43d040a66b3ca9bd85234d624a0786603712ce406f51e14a646b71b01c80de8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()



oath2scheme = OAuth2PasswordBearer(tokenUrl="auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Auth
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oath2scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return schemas.User(name=user.name,username=user.username, address=user.address, id=user.id)


@app.post("/auth", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW_Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# User
@app.get("/users/me/", response_model=schemas.User, tags=["Users"])
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.post("/users/register/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.register_user(db=db, user=user)




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

@app.post("/product_types/{product_type_name}/categories", response_model=schemas.ProductType, tags=["Product Types"])
def write_category_to_product_type(product_type_name: str, categories: List[schemas.CategoryCreate], db: Session = Depends(get_db)):
    db_product_type = crud.get_product_type_by_name(product_type_name=product_type_name, db=db)
    if db_product_type is None:
        raise HTTPException(status_code=400, detail="product_type_not_found")
    return crud.add_category_to_product_type(product_type_name=product_type_name, categories=categories,db=db)

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
    db_product = db.query(models.Product).filter(models.Product.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product Already Exists")
    return crud.create_product(db=db, product=product)


