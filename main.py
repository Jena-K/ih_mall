from fastapi import Depends, FastAPI

# from infrastructure.database.db import database
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database import create_db_and_tables, engine, User
from models import models
from routes.routes import api_router
from starlette.middleware.sessions import SessionMiddleware
from auth.kakao_login import kakao_oauth_router
from auth.naver_login import naver_oauth_router
from app.schemas import UserCreate, UserRead, UserUpdate
from auth.users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

origins = ["http://localhost", "http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1", "http://127.0.0.1:8788", "http://localhost:8788", "https://ieunghieut-frontend.pages.dev"]

app = FastAPI()
# app.include_router(api_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)
app.include_router(kakao_oauth_router, prefix="/auth/kakao", tags=["auth"])
app.include_router(naver_oauth_router, prefix="/auth/naver", tags=["auth"])
app.include_router(api_router, prefix="/profile", tags=["profile"])

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


app.add_middleware(SessionMiddleware, secret_key="549d88-72eb-4c34-ba7d-0c67ebfc0eea")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")