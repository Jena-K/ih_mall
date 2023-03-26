import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Enum, DateTime, Boolean, UUID
from infrastructure.database import Base
from models.enums import RoleType
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

class Profile(Base):
    __tablename__ = "profile_table"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    role = Column(Enum(RoleType), nullable=False, server_default=RoleType.member.name)
    provider = Column(String)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="profile", primaryjoin="User.id == Profile.user_id")
    address = relationship("Address", back_populates="profile")
    creator = relationship("Creator", back_populates="profile")
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
