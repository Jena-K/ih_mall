from fastapi import APIRouter, Depends
from infrastructure.database import User
from routes.mypage.profile import profile_routes, address_routes
from routes.mypage.purchase import cart_routes
from routes.creator import creator_routes, delivery_policy_routes, bank_information_routes
from routes.product import category_routes,product_routes, material_routes, option_routes, product_image_routes, theme_product_routes, theme_routes
from routes.mypage.like import like_routes
from auth.kakao_login import kakao_oauth_router
from auth.naver_login import naver_oauth_router
from auth.google_login import google_oauth_router
from auth.users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
)

api_router = APIRouter()

api_router.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])
api_router.include_router(kakao_oauth_router, prefix="/auth/kakao", tags=["auth"])
api_router.include_router(naver_oauth_router, prefix="/auth/naver", tags=["auth"])
api_router.include_router(profile_routes.router)
api_router.include_router(address_routes.router)
api_router.include_router(creator_routes.router)
api_router.include_router(category_routes.router)
api_router.include_router(product_routes.router)
api_router.include_router(material_routes.router)
api_router.include_router(option_routes.router)
api_router.include_router(like_routes.router)
api_router.include_router(theme_routes.router)
api_router.include_router(theme_product_routes.router)
api_router.include_router(cart_routes.router)
api_router.include_router(delivery_policy_routes.router)
api_router.include_router(bank_information_routes.router)
api_router.include_router(product_image_routes.router)

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

@api_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

