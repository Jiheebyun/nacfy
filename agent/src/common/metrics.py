import psutil
from datetime import datetime

def collect_system_metrics() -> dict:
    """
    현재 시스템의 CPU, 메모리, 디스크, 네트워크 사용량을 수집해 반환합니다.
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": psutil.disk_usage("/").total,
            "used": psutil.disk_usage("/").used,
            "percent": psutil.disk_usage("/").percent,
        },
        "net": psutil.net_io_counters()._asdict(),
    }
