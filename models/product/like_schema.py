from typing import List, Optional
from pydantic import BaseModel

class ToggleLikeDto(BaseModel):
    creator_id: Optional[int]
    product_id: Optional[int]