from fastapi import APIRouter

from .items import router_items

router_v1 = APIRouter(prefix='/v1')
router_v1.include_router(router_items)
