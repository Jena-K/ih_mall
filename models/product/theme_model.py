from sqlalchemy import Column
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship


class ThemeProduct(Base):
    __tablename__ = 'theme_product_table'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product_table.id"))
    theme_id = Column(Integer, ForeignKey("theme_table.id"))


class Theme(Base):
    __tablename__ = 'theme_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_at = Column(Date)
    end_at = Column(Date)
    theme_product = relationship("ThemeProduct", backref="theme")


