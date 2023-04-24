from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from ..models.items import Item, ItemAdd
from ..services.items import ItemsService

router_items = APIRouter(prefix='/items')


@router_items.get('/', response_model=list[Item])
def items_list(items_service: ItemsService = Depends()):
    return items_service.get_list()


@router_items.get('/{nm_id}', response_model=Item)
def item_get(nm_id: int, items_service: ItemsService = Depends()):
    return items_service.get(nm_id)


@router_items.delete('/{nm_id}')
def item_delete(nm_id: int, items_service: ItemsService = Depends()):
    items_service.delete(nm_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_items.post('/', response_model=Item)
def item_add(item_data: ItemAdd, items_service: ItemsService = Depends()):
    return items_service.add_item(item_data)
