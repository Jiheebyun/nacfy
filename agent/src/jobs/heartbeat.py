# src/jobs/heartbeat.py
from ..service.client import send_heartbeat
from ..common.metrics import collect_system_metrics
from ..logger import get_logger

log = get_logger(__name__)

async def heartbeat_job():
    # 1) 시스템 메트릭 수집
    metrics = collect_system_metrics()
    log.info("collected system metrics: %s", metrics)

    # 2) 중앙 서버로 전송
    success = await send_heartbeat(metrics)
    if success:
        log.info("heartbeat sent successfully")
    else:
        log.error("heartbeat send failed")
