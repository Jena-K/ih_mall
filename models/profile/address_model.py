import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from infrastructure.database import Base
from sqlalchemy.schema import ForeignKey
from models.profile.profile_model import Profile


class Address(Base):
    __tablename__ = "address_table"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profile_table.id"))
    profile = relationship("Profile", back_populates="address")
    address = Column(String)
    detailed_address = Column(String)
    receiver_name = Column(String)
    phone = Column(String)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    updated_at = Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )
