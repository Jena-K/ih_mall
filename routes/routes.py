from fastapi import APIRouter
from routes.profile import profile_routes

api_router = APIRouter()
api_router.include_router(profile_routes.router)
