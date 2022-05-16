from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)


category_product_type = Table("category_product_type", Base.metadata,
    Column("product_type_id", Integer, ForeignKey("product_types.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)



class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    categories = relationship("Category", secondary=category_product_type, backref="product_types")


order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    product_type_name = Column(String, ForeignKey("product_types.name"))
    brand_name = Column(String, ForeignKey("brands.name"))
    category_name = Column(String, ForeignKey("categories.name"))

    product_type = relationship("ProductType")
    brand = relationship("Brand")
    category = relationship("Category")


# class Association(Base):
#     __tablename__ = "order_product_association"
#
#     order_id = Column(ForeignKey("orders.id"), primary_key=True)
#     product_id = Column(ForeignKey("products.id"), primary_key=True)
#     order = relationship("Order", back_populates="products")
#     product = relationship("Product", back_populates="orders")








class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    name = Column(String)
    address = Column(String)
    hashed_password = Column(String)
    orders = relationship("Order")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    content = Column(String)
    products = relationship("Product", secondary=order_product, backref="orders")



