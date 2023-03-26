import datetime
from infrastructure.database import Base
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "category_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    products = relationship("Product", back_populates="category")
