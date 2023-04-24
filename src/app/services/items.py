from typing import Sequence, Type

import requests
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from ..db import get_session
from ..models.items import ItemAdd, ItemParse
from ..settings import settings
from ..tables import ItemDB


class ParseW:
    ProductUrl: str = settings.PRODUCT_URL
    unit: str = settings.UNIT
    qty_url: str = settings.QUANTITY_URL

    def get_product(self, nm_id: int) -> dict:
        response = requests.get(
            f'{self.ProductUrl}?curr={self.unit}&nm={nm_id}',
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='Request error on wildberries.',
            )
        try:
            products = response.json()['data']['products']
            if not isinstance(products, list):
                raise ValueError
        except (KeyError, ValueError) as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Unexpected response getting product. Err: {str(err)}',
            )
        if len(products) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found.',
            )
        return products[0]

    def get_quantity(self, nm_id: int, op_id: int) -> int:
        form_data: dict = {
            'basketItems[0][cod1S]': nm_id,
            'basketItems[0][chrtId]': op_id,
        }
        response = requests.post(self.qty_url, data=form_data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='request error on wildberries.',
            )
        try:
            quantities: list = (
                response.json()['value']['data']['basket']
                ['basketItems'][0]['stocks']
            )
            if not isinstance(quantities, list):
                raise ValueError
            if len(quantities) == 0:
                return 0
            quantity: int = quantities[0]['qty']
        except (KeyError, IndexError, ValueError) as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Unexpected response getting quantity: {str(err)}',
            )
        return quantity

    def get_option_id(self, product: dict) -> int:
        try:
            option_id = product['sizes'][0]['optionId']
        except (KeyError, IndexError) as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Unexpected response getting op_id: {str(err)}',
            )
        return option_id


class ItemsService:
    def __init__(self):
        self._db: Session = get_session().__next__()

    def _get_by_id(self, nm_id: int) -> Type[ItemDB]:
        return self._db.get(ItemDB, nm_id)

    def get(self, nm_id: int) -> Type[ItemDB]:
        result = self._get_by_id(nm_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    def get_list(self) -> Sequence[ItemDB]:
        return self._db.scalars(select(ItemDB)).all()

    def delete(self, nm_id: int) -> None:
        item = self.get(nm_id)
        self._db.delete(item)
        self._db.commit()

    def create_model(self, nm_id: int) -> ItemParse:
        parser = ParseW()
        product = parser.get_product(nm_id)
        option_id = parser.get_option_id(product)
        product['quantity'] = parser.get_quantity(nm_id, option_id)
        return ItemParse(**product)

    def add_item(self, item_data: ItemAdd) -> ItemDB:
        if self._get_by_id(item_data.nm_id) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Already exists.',
            )
        item = ItemDB(**self.create_model(item_data.nm_id).dict())
        self._db.add(item)
        self._db.commit()
        return item

    def update(self, nm_id: int) -> Type[ItemDB]:
        item = self.get(nm_id)
        new_data = self.create_model(item.nm_id).dict()
        for key, value in new_data.items():
            setattr(item, key, value)
        self._db.commit()
        self._db.refresh(item)
        return item
