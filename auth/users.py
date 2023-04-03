import os
import uuid
from typing import Optional

from fastapi import Depends, Request, status
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx_oauth.clients.google import GoogleOAuth2
from app.db import create_db_and_tables
from infrastructure.database import User, get_async_session, get_user_db
from models.profile.profile_model import Profile
from sqlalchemy.orm.session import Session
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

SECRET = "SECRET"

google_oauth_client = GoogleOAuth2(
    os.getenv("GOOGLE_CLIENT_ID", ""),
    os.getenv("GOOGLE_CLIENT_SECRET", ""),
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        
        print(f"User {user.id} has registered.")
        

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
    
    async def on_after_login(
        self, user:User, token: str, request: Optional[Request] = None
    ):
        print(f"Login user {user.id}. successed token: {token}")
        # redirect_url = URL(request.url_for('/')).include_query_params(msg="Succesfully created!")
        # return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        # return RedirectResponse(url="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
# , headers={"access_token": token, "token_type": "bearer"}

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

