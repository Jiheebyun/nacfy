from ..service.client import fetch_config
from ..logger import get_logger
log = get_logger(__name__)

async def heartbeat_job():
    await fetch_config()          # 예시: 설정을 가져오며 heartbeat 겸용
    log.info("heartbeat sent")
