import functools
import asyncio
from config import broker


def broker_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with broker as br:
            return await func(br, *args, **kwargs)

    return wrapper


async def get_broker():
    async with broker as br:
        yield br


# Пример использования
@broker_session
async def publish_message(br):
    # await br.publish(["Запускаемся в интервале", "interval_schedule"],
    #                channel="scheduler_interval")
    await br.publish({"name": "Petya"}, channel="task_queue")
    # await br.publish("interval_schedule", channel="scheduler_remove_task")


# Основная функция
async def main():
    await publish_message()


# Запуск
asyncio.run(main())
