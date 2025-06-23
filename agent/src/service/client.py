# src/service/client.py
import httpx
from ..config import settings
from ..logger import get_logger

log = get_logger(__name__)

async def fetch_config() -> dict | None:
    """
    중앙-에이전트가 60초마다 호출해
    /api/config/<AGENT_ID> 를 가져오는 헬퍼.
    실패해도 에이전트가 죽지 않도록 None을 돌려준다.
    """
    url = f"{settings.nacfy_server}/api/config/{settings.agent_id}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
            cfg = response.json()
            log.info("config received: %s", cfg)
            return cfg
    except httpx.HTTPError as err:
        log.error("fetch_config failed: %s", err)
        return None

async def send_heartbeat(payload: dict) -> bool:
    """
    수집된 메트릭(payload)을
    /api/heartbeat/<AGENT_ID> 로 POST 전송하는 헬퍼.
    실패해도 에이전트가 죽지 않도록 False를 돌려준다.
    """
    url = f"{settings.nacfy_server}/api/heartbeat/{settings.agent_id}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return True
    except httpx.HTTPError as err:
        log.error("send_heartbeat failed: %s", err)
        return False


# | 상황 | 중앙-에이전트(지금 만들고 있는 FastAPI 프로세스)가 Nacfy 웹-서버와 계속 통신해야 함.<br>예) “내 설정 좀 줘”, “나는 살아 있어(heartbeat)”, “지금 노드가 3개 붙었어” |
# | 문제 | 매번 `httpx.get("http://…/api/config/agent-001")` 를 모든 파일마다 복사/붙여넣기 하면 **중복**·**오타**·**에러 처리 지옥**                      |
# | 헬퍼 | `src/service/client.py` 하나만 만들어 **“REST 호출 공통 함수”** 를 모아 둔다.<br>→ 다른 모듈은 `await fetch_config()` 처럼 **한 줄**만 호출하면 끝.  |
# | 장점 | • 코드 짧아짐<br>• 에러 로그 형식 통일<br>• 추후 토큰/JWT 헤더 추가도 **한 파일**만 바꾸면 됨                                                      |
