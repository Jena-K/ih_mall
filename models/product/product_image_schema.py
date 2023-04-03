import io
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, validator
import os
from PIL import Image

class CreateProductImageDto(BaseModel):
    image: UploadFile


class ResponseCreateProductImageDto(BaseModel):
    id: int
    product_id: int
    url: str

    class Config:
        orm_mode = True

class UpdateProductImageDto(BaseModel):
    id: int
    image: Optional[UploadFile]
    product_id: Optional[int]