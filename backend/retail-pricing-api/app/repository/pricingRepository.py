import datetime
import io
from fastapi import HTTPException, UploadFile
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
    
    async def GetPricingHistory(self, session: AsyncSession, product_id: int, store_id: int):
        try:
            three_months_ago = datetime.date.today() - datetime.timedelta(days=90)

            stmt = (
                select(Pricing)
                .where(
                    Pricing.product_id == product_id,
                    Pricing.store_id == store_id,
                    Pricing.is_active == False,
                    Pricing.effective_date >= three_months_ago
                )
                .order_by(Pricing.effective_date.desc())
            )

            result = await session.execute(stmt)

            records = result.scalars().all()

            return {
                "total": len(records),
                "rows": records
            }
        except Exception as ex:
            raise
    
    
    async def UploadPricingCSVDetails(self, session: AsyncSession, store_id: int, file: UploadFile):
        try:
            if not file.filename.endswith(".csv"):
                raise HTTPException(status_code=400, detail="Only CSV allowed")

            content = await file.read()
            csv_file = io.StringIO(content.decode("utf-8"))
            reader = list(csv.DictReader(csv_file))

            if not reader:
                raise HTTPException(status_code=400, detail="CSV empty")

            # 1: preload all products

            skus = [row["sku"].strip() for row in reader]
            product_stmt = select(Product).where(Product.sku.in_(skus))
            product_result = await session.execute(product_stmt)
            products = product_result.scalars().all()
            product_map = {
                p.sku: p.product_id
                for p in products
            }

            # 2: preload existing pricing

            product_ids = list(product_map.values())
            pricing_stmt = select(Pricing).where(
                Pricing.store_id == store_id,
                Pricing.product_id.in_(product_ids)
            )
            pricing_result = await session.execute(pricing_stmt)
            pricing_rows = pricing_result.scalars().all()

            # map for quick lookup

            pricing_map = {
                (p.product_id, p.effective_date): p
                for p in pricing_rows
            }

            active_map = {
                p.product_id: p
                for p in pricing_rows if p.is_active
            }

            update_list = []
            insert_list = []

            # 3: process CSV rows

            for row in reader:
                sku = row["sku"].strip()
                price = float(row["price"])
                effective_date = datetime.datetime.strptime(
                    row["effective_date"], "%m/%d/%Y"
                ).date()
                product_id = product_map.get(sku)

                if not product_id:
                    continue

                existing = pricing_map.get((product_id, effective_date))
                
                # CASE 1: update existing

                if existing:
                    update_list.append({
                        "id": existing.pricing_id,
                        "price": price
                    })

                # CASE 2: insert new

                else:
                    active = active_map.get(product_id)
                    if active:
                        update_list.append({
                            "id": active.pricing_id,
                            "is_active": False
                        })

                    insert_list.append(
                        Pricing(
                            product_id=product_id,
                            store_id=store_id,
                            price=price,
                            effective_date=effective_date,
                            is_active=True,
                            created_at=datetime.datetime.utcnow()
                        )
                    )

            # 4: execute bulk updates

            for upd in update_list:
                stmt = (
                    update(Pricing)
                    .where(Pricing.pricing_id == upd["id"])
                    .values(**{k: v for k, v in upd.items() if k != "id"})
                )

                await session.execute(stmt)

            # 5: bulk insert

            session.add_all(insert_list)
            await session.commit()
            
            return {
                "message": "Upload successful",
                "updated": len(update_list),
                "inserted": len(insert_list)
            }
            
        except Exception as ex:
            raise
        


    