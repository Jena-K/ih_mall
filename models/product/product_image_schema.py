import io
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, validator
import os
from PIL import Image

class CreateProductImage(BaseModel):
    image: UploadFile


class ResponseCreateProductImage(BaseModel):
    # id: int
    # # product_id: int
    # # url: str

    class Config:
        orm_mode = True