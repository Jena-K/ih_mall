
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database import create_db_and_tables, engine, User
from routes.routes import api_router
from starlette.middleware.sessions import SessionMiddleware

origins = ["https://quiet-dawn-85341.herokuapp.com", "http://localhost", "http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1", "http://127.0.0.1:8788", "http://localhost:8788", "https://ieunghieut-frontend.pages.dev"]

app = FastAPI()

app.include_router(api_router)

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