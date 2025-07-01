import subprocess
from typing import List, Dict, Any
from ..logger import get_logger

log = get_logger(__name__)

def check_service_status(service_name: str) -> Dict[str, Any]:
    """
    systemd 서비스의 상태를 확인합니다.
    Returns: {'service': str, 'is_active': bool, 'status_output': str, 'error': str|None}
    """
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        is_active = result.stdout.strip() == 'active'
        status_result = subprocess.run(
            ['systemctl', 'status', service_name, '--no-pager'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            'service': service_name,
            'is_active': is_active,
            'status_output': status_result.stdout,
            'error': None
        }
    except subprocess.TimeoutExpired:
        return {
            'service': service_name,
            'is_active': False,
            'status_output': '',
            'error': 'Timeout checking service status'
        }
    except Exception as e:
        return {
            'service': service_name,
            'is_active': False,
            'status_output': '',
            'error': str(e)
        }

def monitor_services(services: List[str]) -> List[Dict[str, Any]]:
    """
    여러 서비스의 상태를 반복적으로 확인합니다.
    Returns: 각 서비스별 상태 리스트
    """
    results = []
    for svc in services:
        status = check_service_status(svc)
        log.info(f"Service {svc} active: {status['is_active']}")
        if status['error']:
            log.error(f"Service {svc} error: {status['error']}")
        results.append(status)
    return results 