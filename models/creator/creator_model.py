import sqlalchemy
from sqlalchemy import UUID, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship


class Creator(Base):
    __tablename__ = "creator_table"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    phone = Column(String)
    businessNumber = Column(String)
    businessName = Column(String)
    representative = Column(String)
    representativeType = Column(String)
    businessRegistrationCertification = Column(String)
    address = Column(String)
    sns = Column(String)
    is_certified = Column(Boolean, default=False)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="creator", primaryjoin="User.id == Creator.user_id")
    products = relationship("Product", back_populates="creator")
    materials = relationship("Material", back_populates="creator")
    likes = relationship("CreatorLike", back_populates="creator")
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
