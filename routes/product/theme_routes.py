
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.theme_schema import \
    (CreateThemeDto, ResponseCreateThemeDto, UpdateThemeDto, GetThemeDto)
from repositories import theme_repository
from auth.users import current_active_user

router = APIRouter(prefix="/theme", tags=["theme"])


# Theme Registration
@router.post("/create", response_model=ResponseCreateThemeDto)
async def create_theme(request: CreateThemeDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    print(request)
    theme = await theme_repository.create_theme(request, db, current_user)
    return theme


# Theme Update
@router.patch("/update", response_model=ResponseCreateThemeDto)
async def update_theme(request: UpdateThemeDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    theme = await theme_repository.update_theme(request, db, current_user)
    return theme


# Get Theme
@router.get("/", response_model=ResponseCreateThemeDto)
async def get_theme(request: GetThemeDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    theme = await theme_repository.get_theme(request, db, current_user)
    return theme


# Get Theme List
@router.get("/list", response_model=List[ResponseCreateThemeDto])
async def get_theme_list(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    themes = await theme_repository.get_theme_list(db, current_user)
    return themes

