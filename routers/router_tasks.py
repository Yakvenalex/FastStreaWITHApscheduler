from faststream.redis import RedisRouter

router = RedisRouter(prefix="task_")


@router.subscriber("queue")
async def process_task(data: dict):
    try:
        print(f"Выполняю задачу: {data}")
        # Ваш код обработки задачи здесь
    except Exception as e:
        print(f"Ошибка при выполнении задачи: {e}")
