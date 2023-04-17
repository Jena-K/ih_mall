
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.theme_schema import \
     CreateThemeProductDto, ResponseCreateThemeProductDto, ThemeProductIdDto, ThemeProductIdDto
from repositories import theme_repository
from auth.users import current_active_user

router = APIRouter(prefix="/theme_product", tags=["theme"])


# Theme Product Registration
@router.post("/create", response_model=ResponseCreateThemeProductDto)
async def create_theme_product(request: CreateThemeProductDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    theme = await theme_repository.create_theme_product(request, db, current_user)
    return theme


# Theme Product Update
@router.post("/delete", response_model=dict)
async def update_theme_product(request: ThemeProductIdDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    theme = await theme_repository.delete_theme_product(request, db, current_user)
    return theme


# Get Theme Product
@router.get("/", response_model=ResponseCreateThemeProductDto)
async def get_theme_product(request: ThemeProductIdDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    theme = await theme_repository.get_theme_product(request, db, current_user)
    return theme


# Get Theme Product List
@router.get("/list", response_model=List[ResponseCreateThemeProductDto])
async def get_theme_product_list(request: ThemeProductIdDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    themes = await theme_repository.get_theme_product_list(request, db, current_user)
    return themes
