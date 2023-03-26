import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from infrastructure.database import Base
from sqlalchemy.schema import ForeignKey


class Address(Base):
    __tablename__ = "address_table"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="address", primaryjoin="User.id == Address.user_id")
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
