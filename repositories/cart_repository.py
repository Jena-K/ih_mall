
from sqlalchemy import select, and_, or_, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User
from models.profile.cart_schema import CreateCartDto, ItemDTO, DeleteCartDto, UpdateCartDTO, ResponseCartListDTO
from models.profile.cart_model import Cart
from models.product.product_model import Product
from collections import defaultdict


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


async def get_cart(db: AsyncSession, current_user: User):

    response = defaultdict(list)

    cart_items = await db.execute(
        select(Cart)
        .options(selectinload(Cart.product).selectinload(Product.creator))
        .where(Cart.user_id == current_user.id)
    )

    cart_items = cart_items.scalars().all()

    # print(test.scalars().all()[0].values())
    # creators = [{'creator_id': i.product.creator.id, 'nickname': i.product.creator.nickname} for i in cart_items.scalars().all()]
    # temp = ResponseCartListDTO()
    # creators = [{i.product.creator.nickname: defaultdict(list)} for i in cart_items]
    # creators = set([i.product.creator.nickname for i in cart_items])
    # for creator in creators:
    #     print(creator)
    response = {j: [] for j in set([i.product.creator.nickname for i in cart_items])}
    print(response)
    # response['Jena'].append(1)
    # for i in cart_items:
        # response['hi'].append(1)

    for i in cart_items:
        response[i.product.creator.nickname].append(i)
    # ResponseCartListDTO.items.append()
    print(response)
    return {'result': 'success'}
