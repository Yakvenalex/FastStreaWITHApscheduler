from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from faststream.redis import RedisRouter
from config import scheduler


router = RedisRouter(prefix="scheduler_")


async def my_schedule_task(my_text: str):
    print(my_text)


@router.subscriber("date")
async def test_schedule():
    run_time = datetime.now() + timedelta(seconds=30)
    scheduler.add_job(my_schedule_task, trigger="date", run_date=run_time)


@router.subscriber("cron")
async def schedule_cron_task():
    # Задача будет выполняться каждую минуту
    scheduler.add_job(my_schedule_task,
                      trigger=CronTrigger(minute='*'))  # Каждую минуту


@router.subscriber("cron_daily")
async def schedule_cron_daily_task():
    # Задача будет выполняться каждый день в 14:30
    scheduler.add_job(my_schedule_task,
                      trigger=CronTrigger(hour=14, minute=30))  # Каждый день в 14:30


@router.subscriber("interval")
async def schedule_interval_task(my_text: str, task_id: str):
    # Задача будет выполняться каждые 10 секунд
    scheduler.add_job(func=my_schedule_task,
                      args=[my_text],
                      trigger="interval",
                      seconds=10,
                      id=task_id)  # Каждые 10 секунд


@router.subscriber("remove_task")
async def remove_scheduled_task(task_id: str):
    scheduler.remove_job(task_id)
    print(f"Задача {task_id} удалена.")
