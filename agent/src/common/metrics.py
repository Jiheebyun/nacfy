import psutil
from datetime import datetime
from typing import Dict, List, Any

def collect_system_metrics() -> dict:
    """
    현재 시스템의 CPU, 메모리, 디스크, 네트워크 사용량을 수집해 반환합니다.
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "memory": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent,
            "swap_total": psutil.swap_memory().total,
            "swap_used": psutil.swap_memory().used,
            "swap_percent": psutil.swap_memory().percent,
        },
        "disk": {
            "total": psutil.disk_usage("/").total,
            "used": psutil.disk_usage("/").used,
            "free": psutil.disk_usage("/").free,
            "percent": psutil.disk_usage("/").percent,
        },
        "network": psutil.net_io_counters()._asdict(),
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
    }

def collect_detailed_disk_metrics() -> List[Dict[str, Any]]:
    """
    모든 마운트 포인트의 디스크 사용량을 수집합니다.
    """
    disk_metrics = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_metrics.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except (PermissionError, FileNotFoundError):
            continue
    return disk_metrics

def collect_process_metrics() -> Dict[str, Any]:
    """
    프로세스 관련 메트릭을 수집합니다.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # CPU/메모리 사용량 상위 10개 프로세스
    top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
    top_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:10]
    
    return {
        "total_processes": len(processes),
        "top_cpu_processes": top_cpu,
        "top_memory_processes": top_memory,
    }
