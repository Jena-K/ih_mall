import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship


class Material(Base):
    __tablename__ = "material_table"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_table.id"))
    creator = relationship("Creator", back_populates="materials")
    products = relationship("Product", back_populates="material")
    name = Column(String)
    material = Column(String)
    coating = Column(String)
    size = Column(String)
    origin = Column(String)
    caution = Column(String)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
    )
    updated_at = Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )
