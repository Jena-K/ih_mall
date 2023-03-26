from typing import AsyncGenerator, List

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship

import os
from dotenv import load_dotenv


load_dotenv()

environment = os.environ.get('ENVIRONMENT')

host = None
user = None
password = None
db_name = None

if environment == 'production':
    host = os.environ.get('HEROKU_CLIENT_HOST')
    user = os.environ.get('HEROKU_CLIENT_USERNAME')
    password = os.environ.get('HEROKU_CLIENT_PASSWORD')
    db_name = os.environ.get('HEROKU_CLIENT_DB_NAME')
else:
    host = os.environ.get('LOCAL_DATABASE_HOST')
    user = os.environ.get('LOCAL_DATABASE_USER')
    password = os.environ.get('LOCAL_DATABASE_PASSWORD')
    db_name = os.environ.get('LOCAL_DATABASE_DB_NAME')



DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{host}:5432/{db_name}'

class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    
    

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)