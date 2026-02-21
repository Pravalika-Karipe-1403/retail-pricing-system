from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import csv

from db.retail_db_entities import Pricing, Product
from schema.pricing_schema import PricingListResponse


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
                Product.sku,
                Product.product_name,
                Pricing.price,
                Pricing.effective_date
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