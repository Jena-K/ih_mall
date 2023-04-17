from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.creator.bank_information_schema import CreateBankInformationDto, CreateResponseBankInformationDto, UpdateBankInformationDto

from repositories import bank_information_repository
from auth.users import current_active_user

router = APIRouter(prefix="/bank_information", tags=["bank_information"])


# 은행정보 등록
@router.post("/", response_model=CreateResponseBankInformationDto)
async def create_bank_information(request: CreateBankInformationDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    bank_information = await bank_information_repository.create_bank_information(db, current_user, request)
    return bank_information


# 은행정보 업데이트
@router.patch("/", response_model=CreateResponseBankInformationDto)
async def update_bank_information(request: UpdateBankInformationDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    bank_information = await bank_information_repository.update_bank_information(db, current_user, request)
    return bank_information


# 은행정보 조회 (Single)
@router.get("/", response_model=CreateResponseBankInformationDto)
async def get_bank_information(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    bank_information = await bank_information_repository.get_bank_information(db, current_user)
    return bank_information
