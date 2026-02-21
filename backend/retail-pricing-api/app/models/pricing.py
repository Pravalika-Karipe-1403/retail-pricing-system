from pydantic import BaseModel
from sqlalchemy import Column, BigInteger, Integer, DECIMAL, Date, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func


class Pricing(BaseModel):

    __tablename__ = "pricing"
    pricing_id = Column(BigInteger, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"))
    store_id = Column(BigInteger)
    price = Column(DECIMAL(10,2))
    effective_date = Column(Date)
    effective_to = Column(Date)
    batch_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())