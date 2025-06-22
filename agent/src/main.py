from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .config import settings
from .logger import get_logger
from .jobs.heartbeat import heartbeat_job

log = get_logger(__name__)
app = FastAPI(title="nacfy-agent")
sched = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    log.info("⏳ scheduler init")
    sched.add_job(
        heartbeat_job,
        trigger=IntervalTrigger(seconds=settings.fetch_interval),
        id="heartbeat",
        max_instances=1,
        coalesce=True,
        misfire_grace_time=15,
    )
    sched.start()

@app.get("/ping")
def ping():
    return {"ok": True}
