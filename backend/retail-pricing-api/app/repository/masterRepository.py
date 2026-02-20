from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.retail_db_entities import City, Country, Store

class masterRepository:
    def __init__(self) -> None:
        pass
    
    async def GetCountriesList(self, session: AsyncSession):
        try:
            stmt = (select(Country.country_id, Country.country_name)
                    .order_by(Country.country_name.asc()))
            result = await session.execute(stmt)
            country_list = [{"country_id": row.country_id, "country_name": row.country_name} 
                    for row in result.all()]
            return country_list
        except Exception as ex:
            raise
        
    async def GetCityList(self, session: AsyncSession, countryId: int):
        try:
            stmt = (select(City.city_id, City.city_name).where(City.country_id == countryId)
                    .order_by(City.city_name.asc()))
            result = await session.execute(stmt)
            city_list = [{"city_id": row.city_id, "city_name": row.city_name} 
                    for row in result.all()]
            return city_list
        except Exception as ex:
            raise
        
    async def GetStoreList(self, session: AsyncSession, cityId: int):
        try:
            stmt = (select(Store.store_id, Store.store_name).where(Store.city_id == cityId)
                    .order_by(Store.store_name.asc()))
            result = await session.execute(stmt)
            store_list = [{"store_id": row.store_id, "store_name": row.store_name} 
                    for row in result.all()]
            return store_list
        except Exception as ex:
            raise