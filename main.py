import asyncio
from faststream import FastStream
from config import scheduler, broker
from routers.router_tasks import router as router_task
from routers.router_scheduler import router as router_scheduler
from loguru import logger

# Инициализация брокера и FastStream
app = FastStream(broker)


@app.after_startup
async def startup_tasks():
    logger.info("FastStream успешно запущен, планировщик задач инициализируется...")
    scheduler.start()


@app.after_shutdown
async def shutdown_tasks():
    logger.info("Останавливаю планировщик задач...")

    # Удаляем все задачи из планировщика
    scheduler.remove_all_jobs()

    # Останавливаем планировщик
    scheduler.shutdown()


async def register_app():
    broker.include_router(router_task)
    broker.include_router(router_scheduler)
    await app.run()


if __name__ == '__main__':
    try:
        asyncio.run(register_app())
    except KeyboardInterrupt:
        logger.info("Остановка приложения...")
