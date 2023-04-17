
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User
from models.product.theme_model import ThemeProduct, Theme
from models.product.theme_schema import (
    CreateThemeDto, UpdateThemeDto, GetThemeDto,
     CreateThemeProductDto, ThemeProductIdDto, ThemeProductIdDto)


async def create_theme(request: CreateThemeDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    new_theme = Theme(
        name=request.name,
        start_at=request.start_at,
        end_at=request.end_at,
    )

    db.add(new_theme)
    await db.commit()
    await db.refresh(new_theme)

    return new_theme


async def update_theme(request: UpdateThemeDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    theme = await db.execute(
        select(Theme)
        .where(Theme.id == request.id)
    )
    theme = theme.scalar_one_or_none()

    if theme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(theme, key, value)

    await db.commit()
    await db.refresh(theme)

    return theme


async def get_theme(request: GetThemeDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    theme = await db.execute(
        select(Theme)
        .where(Theme.id == request.id)
    )

    theme2 = await db.execute(
        select(Theme)
        .where(Theme.id == request.id)
        .options(selectinload(Theme.theme_product))
    )

    # theme2 = theme2.scalar_one_or_none()
    # print(theme2.scalars().all())
    # for i in theme2.scalar().theme_product:
        # print(i.product_id)
    # print(a)
    # for i in theme2.fetchall():
        # print(i[0].id)
    '''
    from sqlalchemy.orm import selectinload

    async with session.begin():
    user = await session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    if user is None:
        return None

    posts = await session.execute(
        select(Post).options(selectinload(Post.user)).where(Post.user_id == user_id)
    ).scalars().all()

    return posts


    '''

    # print(theme2.theme_product)
    # theme2 = theme2.scalar_one_or_none()
    # print(theme2.theme_product)

    theme = theme.scalar_one_or_none()

    if theme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")

    return theme


async def get_theme_list(db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    theme = await db.execute(
        select(Theme)
    )

    theme_list = theme.scalars()

    themes = [themes for themes in theme_list]

    return themes


async def create_theme_product(request: CreateThemeProductDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    new_theme_product = ThemeProduct(
        product_id=request.product_id,
        theme_id=request.theme_id
    )

    db.add(new_theme_product)
    await db.commit()
    await db.refresh(new_theme_product)

    return new_theme_product


#수정 필요
async def delete_theme_product(request: ThemeProductIdDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    theme_product = await db.get(ThemeProduct, request.id)

    if theme_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ThemeProduct not found")

    await db.execute(
        delete(ThemeProduct)
        .where(ThemeProduct.id == request.id)
    )
    # theme_product = await db.execute(
    #     select(ThemeProduct)
    #     .where(ThemeProduct == request.id)
    # )
    # theme_product = theme_product.fetchone()

    await db.commit()

    return {'result': 'success'}


async def get_theme_product_list(request: ThemeProductIdDto, db: AsyncSession, current_user: User):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    theme_product = await db.execute(
        select(ThemeProduct)
        .where(ThemeProduct.theme_id == request.id)
    )

    theme_product_list = theme_product.scalars()

    theme_products = [theme_products for theme_products in theme_product_list]

    return theme_products