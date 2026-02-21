from pydantic import BaseModel
from datetime import date


class PricingResponse(BaseModel):
    pricing_id: int
    sku: str
    product_name: str
    price: float
    effective_date: date


class PricingListResponse(BaseModel):
    rows: list
    total: int