from fastapi import APIRouter
from routes.mypage.profile import profile_routes, address_routes
from routes.mypage.purchase import cart_routes
from routes.creator import creator_routes, delivery_policy_routes, bank_information_routes
from routes.product import category_routes,product_routes, material_routes, option_routes, product_image_routes, theme_product_routes, theme_routes
from routes.mypage.like import like_routes

api_router = APIRouter()
route_modules = [profile_routes,
                 address_routes,
                 creator_routes,
                 category_routes,
                 product_routes,
                 material_routes,
                 option_routes,
                 like_routes,
                 theme_routes,
                 theme_product_routes,
                 cart_routes,
                 delivery_policy_routes,
                 bank_information_routes,
                 product_image_routes,
                 ]

for i in route_modules:
    api_router.include_router(i.router)


