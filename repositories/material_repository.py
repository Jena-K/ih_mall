from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from models.product.material_model import Material
from models.product.material_schema import CreateMaterialDto, UpdateMaterialDto
from sqlalchemy.orm import selectinload

async def create_material(db: AsyncSession, current_user: User, request: Optional[CreateMaterialDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    new_material = Material(
        creator_id=creator.id,
        name=request.name,
        material=request.material,
        coating=request.coating,
        size=request.size,
        origin=request.origin,
        caution=request.caution
    )
    db.add(new_material)
    await db.commit()
    await db.refresh(new_material)
    
    return new_material

# Update Material
async def update_material(db: AsyncSession, current_user: User, request: Optional[UpdateMaterialDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")


    material = await db.execute(
        select(Material)
        .options(selectinload(Material.creator))
        .where(Material.creator_id == creator.id)
        .where(Material.id == request.id)
    )
    material = material.scalar_one_or_none()

    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    for key, value in request:
        if value is not None:
            setattr(material, key, value)
    
    await db.commit()
    await db.refresh(material)
    
    return material

# Get Material (Single)
async def get_material(db: AsyncSession, request: Optional[UpdateMaterialDto]):

    material = await db.execute(
        select(Material)
        .where(Material.id == request.id)
    )

    material = material.scalar_one_or_none()


    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
    return material


# Get Materials (List)
async def get_materials(db: AsyncSession):
    
    materials = await db.execute(
        select(Material)
    )
    
    materials = materials.scalars()
    
    if materials is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material list not found")
    
    else:
        materials = [material for material in materials]
    
    return materials