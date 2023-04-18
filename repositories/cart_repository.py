
from sqlalchemy import select, and_, or_, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User
from models.profile.cart_schema import CreateCartDto, DeleteCartDto, UpdateCartDTO, ResponseCartDTO, SimpleCartItemDto
from models.profile.cart_model import Cart
from models.creator.creator_schema import SimpleCreatorDTO
from models.product.product_model import Product
from collections import defaultdict
import jsonschema, json

async def add_cart(request: CreateCartDto, db: AsyncSession, current_user: User):

    for option in request.options:
        item = await db.execute(
            select(Cart)
            .where(
                and_(
                    Cart.user_id == current_user.id,
                    Cart.product_id == request.product_id,
                    Cart.option_id == option.option_id,
                    Cart.cnt == option.cnt
                )
            )
        )
        item = item.scalar_one_or_none()
        if item:
             await db.execute(
                 update(Cart)
                 .where(
                    Cart.user_id == current_user.id,
                    Cart.product_id == request.product_id,
                    Cart.option_id == option.option_id
                 )
                 .values(cnt=Cart.cnt + option.cnt)
             )
        else:
            add_item = Cart(
                user_id=current_user.id,
                product_id=request.product_id,
                option_id=option.option_id,
                cnt=option.cnt
            )
            db.add(add_item)

    await db.commit()

    return {'result': 'success'}


async def delete_cart(request: DeleteCartDto, db: AsyncSession, current_user: User):

    await db.execute(
        delete(Cart)
        .where(
            and_(
                Cart.id.in_(request.ids),
                Cart.user_id == current_user.id
            )
        )
    )
    await db.commit()

    return {'result': 'success'}


async def update_cart(request: UpdateCartDTO, db: AsyncSession, current_user: User):

    await db.execute(
        update(Cart)
        .where(
            Cart.id == request.id,
            Cart.user_id == current_user.id
        )
        .values(cnt=request.cnt)
    )

    await db.commit()

    return {'result': 'success'}


# 장바구니에서 제품 목록을 작가 별로 묶어서 리턴
async def get_cart(db: AsyncSession, current_user: User):

    item_dict = defaultdict(list)
    response_item = []
    cart_items = await db.execute(
        select(Cart)
        .options(selectinload(Cart.product).selectinload(Product.creator))
        .options(selectinload(Cart.product).selectinload(Product.options))
        .where(Cart.user_id == current_user.id)
    )
    for i in cart_items.scalars().all():
        creator = (
            i.product.creator.id,
            i.product.creator.nickname
        )

        item = {
            'id': i.id,
            'product_id': i.product.id,
            'name': i.product.name,
            'price': i.product.price,
            'option_id': i.option.id,
            'option_name': i.option.name,
            'cnt': i.cnt}

        item_dict[creator].append(item)

    for key, val in item_dict.items():
        response_item.append({'creator_id': key[0], 'nickname': key[1], 'items:': val})

    return response_item
