from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.material_schema import CreateMaterialDto, ResponseCreateMaterialDto, UpdateMaterialDto
from repositories import material_repository
from auth.users import current_active_user

router = APIRouter(prefix="/material", tags=["material"])

# Create Material
@router.post("/", response_model=ResponseCreateMaterialDto)
async def create_material(request: CreateMaterialDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    material = await material_repository.create_material(db, current_user, request)
    return material

# Update material
@router.patch("/update", response_model=ResponseCreateMaterialDto)
async def create_category(request: UpdateMaterialDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    material = await material_repository.update_material(db, current_user, request)
    return material

# Get material
@router.get("/", response_model=ResponseCreateMaterialDto)
async def update_address(request: UpdateMaterialDto, db: Session = Depends(get_async_session)):
    material = await material_repository.get_material(db, request)
    return material

# # Get material List
@router.get("/material_all", response_model=List[ResponseCreateMaterialDto])
async def update_address(db: Session = Depends(get_async_session)):
    materials = await material_repository.get_materials(db)
    return materials