from asyncio.log import logger
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from repository.masterRepository import masterRepository
from db.database import session

master_router = APIRouter(prefix="/Master", tags=["Master"])
_masterRepository = masterRepository()

@master_router.get(path='/GetCountryList')
async def GetCountryList(session: session) -> list:
    try:       
        response = await _masterRepository.GetCountriesList(session)
        return response

    except Exception as ex:
        logger.error(f"Error in GetCountryList: {ex}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while fetching Country List")
  
@master_router.get(path='/GetCityList')
async def GetCityList(session: session, countryId: int) -> list:
    try:       
        response = await _masterRepository.GetCityList(session, countryId)
        return response

    except Exception as ex:
        logger.error(f"Error in GetCityList: {ex}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while fetching City List")
   
@master_router.get(path='/GetStoreList')
async def GetStoreList(session: session, cityId: int) -> list:
    try:       
        response = await _masterRepository.GetStoreList(session, cityId)
        return response

    except Exception as ex:
        logger.error(f"Error in GetStoreList: {ex}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while fetching Store List")
   