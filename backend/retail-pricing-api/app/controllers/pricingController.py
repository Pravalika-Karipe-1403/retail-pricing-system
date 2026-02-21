from asyncio.log import logger
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from repository.masterRepository import masterRepository
from db.database import session
from repository.pricingRepository import pricingRepository
from schema.pricing_schema import PricingBulkUpdateRequest, PricingListResponse

_pricingRepository = pricingRepository()
pricing_router = APIRouter(prefix="/Pricing", tags=["Pricing"])

@pricing_router.get(path='/GetPricingDetails')
async def GetPricingDetails(
    session: session,
    store_id: int,
    page: int = 1,
    page_size: int = 10,
    product: str = ""
    ) -> PricingListResponse:
    try:       
        response = await _pricingRepository.GetPricingDetails(session, store_id, page, page_size, product)
        return response

    except Exception as ex:
        logger.error(f"Error in GetPricingDetails: {ex}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while fetching Pricing List")
 
@pricing_router.put(path="/BulkUpdate")
async def BulkUpdatePricing(
    request: PricingBulkUpdateRequest,
    session: session
):
    try:
        response = await _pricingRepository.BulkUpdatePricing(session, request)
        return response
    except Exception as ex:
        await session.rollback()
        return {
            "success": False,
            "message": str(ex)
        }