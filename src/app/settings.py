from pydantic import BaseSettings


class Settings(BaseSettings):
    MEDIA_DIR: str = 'src/media'
    BACKEND_SERVER: str = '0'
    BACKEND_PORT: int = 8000

    POSTGRES_DB: str = 'db'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_SERVER: str = 'postgres'
    DB_PORT = 5432
    DATABASE_URL: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}'

    PRODUCT_URL: str = 'https://card.wb.ru/cards/detail'
    UNIT: str = 'rub'
    QUANTITY_URL: str = 'https://ru-basket-api.wildberries.ru/webapi/lk/basket/data'


settings: Settings = Settings()
