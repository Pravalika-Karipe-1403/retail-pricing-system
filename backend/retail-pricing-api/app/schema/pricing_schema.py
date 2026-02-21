from pydantic import BaseModel
from datetime import date
from typing import List


class PricingResponse(BaseModel):
    pricing_id: int
    sku: str
    product_name: str
    price: float
    effective_date: date


class PricingListResponse(BaseModel):
    rows: list
    total: int
    
class PricingUpdateItem(BaseModel):
    id: int
    product_id: int
    store_id: int
    price: float
    effective_date: date
    is_active: bool

class PricingBulkUpdateRequest(BaseModel):
    items: List[PricingUpdateItem]