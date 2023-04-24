# Legsy_Test_Task

### Тестовое задание

Для запуска, скачать репозиторий выполнить следующие команды.(для Windows)

``` docker compose up -d ```

После завершения сборки контейнеров выполнить миграции:

``` docker compose exec backend alembic upgrade head ```

Документация будет доступна по URL:

http://127.0.0.1:8000/docs