from sqlalchemy import select, func, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import csv

from db.retail_db_entities import Pricing, Product
from schema.pricing_schema import PricingBulkUpdateRequest, PricingListResponse


class pricingRepository:
    
    def __init__(self):
        pass

    # FETCH LATEST PRICING

    async def GetPricingDetails(
        self,
        db: AsyncSession,
        store_id: int,
        page: int,
        page_size: int,
        product_filter: str
    ) -> PricingListResponse:


        subquery = (
            select(
                Pricing.product_id,
                func.max(Pricing.effective_date).label("max_date")
            )
            .where(
                Pricing.store_id == store_id,
                Pricing.is_active == True
            )
            .group_by(Pricing.product_id)
        ).subquery()
        query = (
            select(
                Pricing.pricing_id,
                Pricing.product_id,
                Pricing.store_id,
                Product.sku,
                Product.product_name,
                Pricing.price,
                Pricing.effective_date,
                Pricing.is_active
            )
            .join(Product)
            .join(
                subquery,
                (Pricing.product_id == subquery.c.product_id)
                & (Pricing.effective_date == subquery.c.max_date)
            )
            .where(Pricing.store_id == store_id)
        )

        if product_filter:
            query = query.where(
                Product.product_name.like(f"%{product_filter}%")
            )

        total = await db.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.order_by(desc(Pricing.effective_date))
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        rows = [dict(row) for row in result.mappings().all()]
        return {
            "rows": rows,
            "total": total
        }

    
    async def BulkUpdatePricing(self, session: AsyncSession, request: PricingBulkUpdateRequest):
        try:
            for item in request.items:
                
                # check if pricing_id exists
                stmt = (
                    select(Pricing).where(Pricing.product_id == item.product_id)
                    .where(Pricing.store_id == item.store_id)
                    .where(Pricing.is_active == True)
                )
                result = await session.execute(stmt)
                existing = result.scalars().first()
                
                # 1. No record exists in table -> insert new record
                if not existing:
                    new_price = Pricing(
                        pricing_id =item.id,
                        price = item.price,
                        effective_date=item.effective_date,
                        is_active=True,
                        created_by='Pravalika'
                    )
                    session.add(new_price)
                    continue
                
                # 2. Same effective_date update existing record
                if existing.effective_date == item.effective_date:
                    stmt = (
                        update(Pricing).where(Pricing.product_id == item.product_id,
                                              Pricing.store_id == item.store_id,
                                              Pricing.is_active == True)
                        .values(
                            price=item.price,
                            updated_by='Pravalika'
                        )
                    )
                    await session.execute(stmt)
                    
                # 3. Effective date different -> New version, old record is_active false
                else:
                    # old record
                    stmt = (
                        update(Pricing).where(Pricing.product_id == item.product_id,
                                              Pricing.store_id == item.store_id,
                                              Pricing.is_active == True)
                        .values(
                            is_active=False,
                            updated_by='Pravalika'
                        )
                    )
                    await session.execute(stmt)
                    
                    # new version -> insert new record
                    new_price = Pricing(
                        pricing_id =item.id,
                        price = item.price,
                        effective_date=item.effective_date,
                        is_active=True,
                        created_by='Pravalika'
                    )
                    
                    session.add(new_price)
            await session.commit()
            
            return {
                "success": True,
                "message": "Pricing updated successfully"
            }
        except Exception as ex:
            raise
    
    # CSV UPLOAD


    async def upload_csv(

        self,
        db: AsyncSession,
        store_id: int,
        file

    ):


        batch_id = str(uuid.uuid4())


        reader = csv.DictReader(file.file.read().decode().splitlines())


        pricing_list = []


        for row in reader:


            pricing = Pricing(

                product_id=row["product_id"],

                store_id=store_id,

                price=row["price"],

                effective_date=row["effective_date"],

                batch_id=batch_id

            )


            pricing_list.append(pricing)


        db.add_all(pricing_list)


        await db.commit()


        return batch_id


    # ROLLBACK


    async def rollback(

        self,
        db: AsyncSession,
        batch_id: str
    ):


        query = (

            select(Pricing)

            .where(Pricing.batch_id == batch_id)

        )


        result = await db.execute(query)


        rows = result.scalars().all()


        for row in rows:

            row.is_active = False


        await db.commit()