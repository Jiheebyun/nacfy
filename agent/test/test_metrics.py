#!/usr/bin/env python3
"""
메트릭 수집 기능 테스트 스크립트
Mac 환경에서 Debian 컨테이너 내부의 에이전트 기능을 테스트합니다.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from common.metrics import collect_system_metrics, collect_detailed_disk_metrics, collect_process_metrics
import json
from datetime import datetime

def test_system_metrics():
    """시스템 메트릭 수집 테스트"""
    print("🔍 시스템 메트릭 수집 테스트...")
    
    try:
        metrics = collect_system_metrics()
        print("✅ 시스템 메트릭 수집 성공")
        print(f"📊 CPU 사용률: {metrics['cpu_percent']}%")
        print(f"📊 메모리 사용률: {metrics['memory']['percent']}%")
        print(f"📊 디스크 사용률: {metrics['disk']['percent']}%")
        print(f"📊 네트워크 패킷: {metrics['network']['packets_sent']} sent, {metrics['network']['packets_recv']} received")
        
        return True
    except Exception as e:
        print(f"❌ 시스템 메트릭 수집 실패: {e}")
        return False

def test_disk_metrics():
    """디스크 메트릭 수집 테스트"""
    print("\n🔍 디스크 메트릭 수집 테스트...")
    
    try:
        disk_metrics = collect_detailed_disk_metrics()
        print(f"✅ 디스크 메트릭 수집 성공: {len(disk_metrics)}개 파티션")
        
        for disk in disk_metrics:
            print(f"  📁 {disk['mountpoint']}: {disk['percent']}% 사용")
        
        return True
    except Exception as e:
        print(f"❌ 디스크 메트릭 수집 실패: {e}")
        return False

def test_process_metrics():
    """프로세스 메트릭 수집 테스트"""
    print("\n🔍 프로세스 메트릭 수집 테스트...")
    
    try:
        process_metrics = collect_process_metrics()
        print(f"✅ 프로세스 메트릭 수집 성공: {process_metrics['total_processes']}개 프로세스")
        
        print("🔥 CPU 사용량 상위 5개 프로세스:")
        for proc in process_metrics['top_cpu_processes'][:5]:
            print(f"  📊 {proc['name']}: {proc['cpu_percent']}%")
        
        print("🔥 메모리 사용량 상위 5개 프로세스:")
        for proc in process_metrics['top_memory_processes'][:5]:
            print(f"  📊 {proc['name']}: {proc['memory_percent']}%")
        
        return True
    except Exception as e:
        print(f"❌ 프로세스 메트릭 수집 실패: {e}")
        return False

def test_heartbeat_simulation():
    """하트비트 시뮬레이션 테스트"""
    print("\n🔍 하트비트 시뮬레이션 테스트...")
    
    try:
        from src.jobs.heartbeat import heartbeat_job
        import asyncio
        
        # 비동기 함수 실행
        result = asyncio.run(heartbeat_job())
        print("✅ 하트비트 시뮬레이션 성공")
        return True
    except Exception as e:
        print(f"❌ 하트비트 시뮬레이션 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 Nacfy Agent 메트릭 테스트 시작")
    print("=" * 50)
    
    tests = [
        ("시스템 메트릭", test_system_metrics),
        ("디스크 메트릭", test_disk_metrics),
        ("프로세스 메트릭", test_process_metrics),
        ("하트비트 시뮬레이션", test_heartbeat_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name} 테스트 중...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📈 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트 통과!")
        return 0
    else:
        print("⚠️  일부 테스트 실패")
        return 1

if __name__ == "__main__":
    exit(main()) 