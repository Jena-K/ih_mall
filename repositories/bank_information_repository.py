from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator, BankInformation
from models.creator.bank_information_schema import CreateBankInformationDto, UpdateBankInformationDto
from sqlalchemy.orm import selectinload

async def create_bank_information(db: AsyncSession, current_user: User, request: Optional[CreateBankInformationDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    new_policy = BankInformation(
        creator_id=creator.id,
        bank_name=request.bank_name,
        account_holder_name = request.account_holder_name,
        account_number = request.account_number,
        is_issue_cash_receipt = request.is_issue_cash_receipt
    )
    db.add(new_policy)
    await db.commit()
    await db.refresh(new_policy)
    
    return new_policy


async def update_bank_information(db: AsyncSession, current_user: User, request: Optional[CreateBankInformationDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")


    bank_information = await db.execute(
        select(BankInformation)
        .options(selectinload(BankInformation.creator))
        .where(BankInformation.creator_id == creator.id)
    )
    bank_information = bank_information.scalar_one_or_none()

    if bank_information is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank information not found")

    for key, value in request:
        if value is not None:
            setattr(bank_information, key, value)
    
    await db.commit()
    await db.refresh(bank_information)
    
    return bank_information

# Get Material (Single)
async def get_bank_information(db: AsyncSession, current_user: User):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")

    bank_information = await db.execute(
        select(BankInformation)
        .where(BankInformation.creator_id == creator.id)
    )

    bank_information = bank_information.scalar_one_or_none()


    if bank_information is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank Information not found")
    return bank_information