from fastapi import APIRouter
from routes.profile import profile_routes, address_routes
from routes.creator import creator_routes
from routes.product import category_routes, product_routes

api_router = APIRouter()
api_router.include_router(profile_routes.router)
api_router.include_router(address_routes.router)
api_router.include_router(creator_routes.router)
api_router.include_router(category_routes.router)
api_router.include_router(product_routes.router)
