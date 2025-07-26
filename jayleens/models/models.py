from .database import Base
import uuid
from sqlalchemy import Column,String,Integer,Boolean,Float,JSON
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy
from sqlalchemy.orm import relationship
import sqlalchemy.orm

class User(Base):
    __tablename__ = "users"

    id = Column(String(32),primary_key=True,nullable=False)
    full_name = Column(String(length=50),nullable=False)
    phone = Column(String(10),nullable=False,unique=True)
    email=sqlalchemy.Column(sqlalchemy.String(length=255),unique=True,index=True)
    password=sqlalchemy.Column(sqlalchemy.String(length=255))
    cart_data = sqlalchemy.Column(JSON,default={})
    joined=sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    def __init__(self,full_name,email,phone,password):
        self.id =uuid.uuid4().hex 
        self.full_name=full_name
        self.email=email
        self.phone = phone
        self.password=password
        self.joined=sqlalchemy.func.now()
    
    def __repr__(self):
        return self.full_name


class Product(Base):
    __tablename__ = "products"
    id=Column(String(32),primary_key=True,nullable=False)
    name = Column(String(length=50),nullable=False)
    image = sqlalchemy.Column(JSON,default={})
    category = Column(String(length=50),nullable=False)
    sub_category = Column(String(length=50),nullable=False)
    price=Column(Float,nullable=False)
    color=Column(String(length=50),nullable=False)
    brand = Column(String(length=50),nullable=False)
    sku= Column(String(length=50),nullable=False)
    vendor = sqlalchemy.Column(sqlalchemy.ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    created_at=sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    def __init__(self,name,category,sub_category,price,color,brand,sku):
        self.id = uuid.uuid4().hex
        self.name=name
        self.category=category
        self.sub_category=sub_category
        self.price=price
        self.color=color
        self.brand =brand
        self.sku = sku
    
    def __repr__(self):
        return self.name


class Cart(Base):
    __tablename__="cart"
    id = sqlalchemy.Column(String(32),primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    item = sqlalchemy.Column(sqlalchemy.ForeignKey("products.id",ondelete="CASCADE"),primary_key=True)
    quantity= Column(Integer, nullable=False)

    def __init__(self,id,user,item):
        self.id = uuid.uuid4().hex
        self.user = user
        self.item = item
    def __repr__(self):
        return self.item


class Order(Base):
    __tablename__="orders"
    id = sqlalchemy.Column(String(32),primary_key=True)
    user= sqlalchemy.Column(sqlalchemy.ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    item = sqlalchemy.Column(sqlalchemy.ForeignKey("cart.item",ondelete="CASCADE"),primary_key=True)
    town=Column(String(30),nullable=F)

    def __init__(self):
        pass

