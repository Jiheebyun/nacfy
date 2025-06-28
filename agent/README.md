# Nacfy Agent

Nacfy Agent는 서버 리소스 모니터링 및 관리를 위한 Python 기반 에이전트입니다.

## 🚀 빠른 시작

### 1. 로컬 개발 환경 (Mac)

```bash
# 1. 가상환경 생성 및 활성화
cd agent
python3 -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
export AGENT_ID=agent-local-001
export NACFY_SERVER=http://localhost:3000
export FETCH_INTERVAL=30

# 4. 에이전트 실행
python -m uvicorn src.main:app --host 0.0.0.0 --port 9010 --reload
```

### 2. Docker 환경 (Debian 시뮬레이션)

```bash
# 1. Docker 이미지 빌드
docker build -t nacfy-agent .

# 2. 컨테이너 실행
docker run -d \
  --name nacfy-agent \
  -p 9010:9010 \
  -e AGENT_ID=agent-docker-001 \
  -e NACFY_SERVER=http://host.docker.internal:3000 \
  -e FETCH_INTERVAL=30 \
  nacfy-agent

# 3. 로그 확인
docker logs -f nacfy-agent
```

### 3. Docker Compose (전체 환경)

```bash
# 1. 전체 서비스 시작
docker-compose up -d

# 2. 서비스 상태 확인
docker-compose ps

# 3. 에이전트 로그 확인
docker-compose logs -f nacfy-agent

# 4. 서비스 중지
docker-compose down
```

## 🧪 테스트

### 로컬 테스트

```bash
# 메트릭 수집 기능 테스트
python test/test_metrics.py

# API 엔드포인트 테스트
curl http://localhost:9010/ping
```

### Docker 컨테이너 내부 테스트

```bash
# 컨테이너 내부 접속
docker exec -it nacfy-agent bash

# 컨테이너 내부에서 테스트 실행
python test/test_metrics.py
```

## 📊 수집되는 메트릭

### 시스템 메트릭
- **CPU**: 사용률, 코어 수, 주파수
- **메모리**: 총량, 사용량, 사용률, 스왑 정보
- **디스크**: 총량, 사용량, 여유공간, 사용률
- **네트워크**: 송수신 패킷, 바이트 수

### 상세 메트릭
- **디스크**: 모든 마운트 포인트별 상세 정보
- **프로세스**: CPU/메모리 사용량 상위 프로세스

## 🔧 설정

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `AGENT_ID` | `agent-001` | 에이전트 고유 ID |
| `NACFY_SERVER` | `http://localhost:3000` | 중앙 서버 URL |
| `FETCH_INTERVAL` | `60` | 메트릭 수집 주기 (초) |

### 설정 파일

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
AGENT_ID=agent-prod-001
NACFY_SERVER=http://nacfy-server.example.com
FETCH_INTERVAL=60
```

## 📡 API 엔드포인트

### GET /ping
에이전트 상태 확인

```bash
curl http://localhost:9010/ping
```

응답:
```json
{
  "ok": true,
  "role": "agent",
  "id": "agent-001"
}
```

## 🔍 문제 해결

### 1. psutil 권한 오류
```bash
# Docker에서 호스트 시스템 정보 접근을 위한 볼륨 마운트
docker run -v /proc:/host/proc:ro -v /sys:/host/sys:ro ...
```

### 2. 네트워크 연결 실패
```bash
# 서버 URL 확인
echo $NACFY_SERVER

# 네트워크 연결 테스트
curl $NACFY_SERVER/ping
```

### 3. 로그 확인
```bash
# Docker 로그
docker logs nacfy-agent

# 로컬 로그 (터미널 출력)
```

## 🏗️ 개발 가이드

### 프로젝트 구조
```
agent/
├── src/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정 관리
│   ├── logger.py            # 로깅 설정
│   ├── common/
│   │   └── metrics.py       # 메트릭 수집
│   ├── jobs/
│   │   └── heartbeat.py     # 주기적 작업
│   └── service/
│       └── client.py        # 서버 통신
├── test/
│   └── test_metrics.py      # 테스트 스크립트
├── Dockerfile               # Docker 이미지
├── docker-compose.yml       # 개발 환경
└── requirements.txt         # Python 의존성
```

### 새로운 메트릭 추가

1. `src/common/metrics.py`에 새로운 수집 함수 추가
2. `src/jobs/heartbeat.py`에서 함수 호출
3. `test/test_metrics.py`에 테스트 추가

### 로컬 vs Docker 테스트

- **로컬**: Mac 환경에서 빠른 개발/디버깅
- **Docker**: Debian 환경에서 실제 배포 환경 테스트

## 📝 로그

에이전트는 다음 정보를 로그로 출력합니다:
- 메트릭 수집 성공/실패
- 서버 통신 상태
- 에러 및 예외 상황
- 스케줄러 동작 상태
