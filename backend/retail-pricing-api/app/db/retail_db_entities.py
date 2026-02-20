from typing import List, Optional

from sqlalchemy import BigInteger, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

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
    country_code: Mapped[str] = mapped_column(String(10))
    country_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    city: Mapped[List['City']] = relationship('City', back_populates='country')


class City(Base):
    __tablename__ = 'city'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['country.country_id'], name='fk_city_country'),
        Index('idx_city_country_id', 'country_id'),
        Index('idx_city_name', 'city_name'),
        Index('uq_city_country', 'city_name', 'country_id', unique=True)
    )

    city_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    country: Mapped['Country'] = relationship('Country', back_populates='city')
    store: Mapped[List['Store']] = relationship('Store', back_populates='city')


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
    store_code: Mapped[str] = mapped_column(String(50))
    store_name: Mapped[str] = mapped_column(String(150))
    city_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_by: Mapped[Optional[str]] = mapped_column(String(100))

    city: Mapped['City'] = relationship('City', back_populates='store')
