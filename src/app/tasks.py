from app.celery import celery_app

from .services.items import ItemsService


@celery_app.task
def update_items():
    try:
        item_service = ItemsService()
        exist_product = item_service.get_list()
        for item in exist_product:
            item_service.update(item.nm_id)
    except Exception as err:
        print(f'Task end with error: {str(err)}')
