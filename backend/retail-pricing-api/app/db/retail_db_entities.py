from typing import Optional
import datetime
import decimal
from sqlalchemy import Boolean

from sqlalchemy import BigInteger, DECIMAL, Date, DateTime, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        Index('idx_country_name', 'country_name'),
        Index('uq_country_code', 'country_code', unique=True),
        Index('uq_country_name', 'country_name', unique=True)
    )

    country_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_code: Mapped[str] = mapped_column(String(10), nullable=False)
    country_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    city: Mapped[list['City']] = relationship('City', back_populates='country')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        Index('idx_product_name', 'product_name'),
        Index('idx_product_name_ft', 'product_name', mysql_prefix='FULLTEXT'),
        Index('sku', 'sku', unique=True)
    )

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    pricing: Mapped[list['Pricing']] = relationship('Pricing', back_populates='product')


class City(Base):
    __tablename__ = 'city'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['country.country_id'], name='fk_city_country'),
        Index('idx_city_country_id', 'country_id'),
        Index('idx_city_name', 'city_name'),
        Index('uq_city_country', 'city_name', 'country_id', unique=True)
    )

    city_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    country: Mapped['Country'] = relationship('Country', back_populates='city')
    store: Mapped[list['Store']] = relationship('Store', back_populates='city')


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['city.city_id'], name='fk_store_city'),
        Index('idx_store_city_id', 'city_id'),
        Index('idx_store_code', 'store_code'),
        Index('idx_store_name', 'store_name'),
        Index('uq_store_code', 'store_code', unique=True)
    )

    store_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    store_code: Mapped[str] = mapped_column(String(50), nullable=False)
    store_name: Mapped[str] = mapped_column(String(150), nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    city: Mapped['City'] = relationship('City', back_populates='store')
    pricing: Mapped[list['Pricing']] = relationship('Pricing', back_populates='store')


class Pricing(Base):
    __tablename__ = 'pricing'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['product.product_id'], ondelete='CASCADE', name='fk_pricing_product'),
        ForeignKeyConstraint(['store_id'], ['store.store_id'], ondelete='CASCADE', name='fk_pricing_store'),
        Index('idx_pricing_batch', 'batch_id'),
        Index('idx_pricing_latest', 'store_id', 'product_id', 'effective_date'),
        Index('idx_pricing_product_effective', 'product_id', 'store_id', 'effective_date')
    )

    pricing_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    store_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    effective_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('1'))
    batch_id: Mapped[Optional[str]] = mapped_column(String(50))
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_by: Mapped[Optional[str]] = mapped_column(String(50))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    product: Mapped['Product'] = relationship('Product', back_populates='pricing')
    store: Mapped['Store'] = relationship('Store', back_populates='pricing')
