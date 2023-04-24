from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, validator


class Item(BaseModel):
    nm_id: int
    name: str
    brand: str
    brand_id: int
    site_brand_id: int
    supplier_id: int
    sale: int
    price: Decimal
    sale_price: Decimal
    rating: float
    feedbacks: int
    colors: Optional[str] = None
    quantity: int

    class Config:
        orm_mode = True


class ItemParse(BaseModel):
    nm_id: int = Field(alias='id')
    name: str
    brand: str
    brand_id: int = Field(alias='brandId')
    site_brand_id: int = Field(alias='siteBrandId')
    supplier_id: int = Field(alias='supplierId')
    sale: int
    price: Decimal = Field(alias='priceU')
    sale_price: Decimal = Field(alias='salePriceU')
    rating: float
    feedbacks: int
    colors: Optional[str] = None
    quantity: int

    @validator('colors', pre=True)
    def color(cls, v):
        if len(v) == 0:
            return None
        return v[0]['name']


class ItemAdd(BaseModel):
    nm_id: int
