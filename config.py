import os

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from faststream.redis import RedisBroker
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )


settings = Settings()
scheduler = AsyncIOScheduler(jobstores={'default': RedisJobStore(host=settings.REDIS_HOST,
                                                                 port=settings.REDIS_PORT,
                                                                 db=settings.REDIS_DB)}
                             )
broker = RedisBroker(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
