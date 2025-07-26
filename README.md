# NACFY

**NACFY** is a self-hosted network access control and monitoring platform.  
It provides centralized configuration management and agent communication for secure server environments.

## 📦 Project Structure
```
nacfy/                         ← 프로젝트 루트
├── agent/                     ← 중앙 에이전트 패키지
│   ├── src/                   ← 에이전트 실제 코드
│   │   ├── ai/                ← AI 기능 모듈
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   └── models.py
│   │   ├── common/            ← 공통 로직 (OS 구분 없는 부분)
│   │   │   ├── __init__.py
│   │   │   └── installer.py
│   │   ├── debian/            ← Debian/Ubuntu 전용 설치 로직
│   │   │   ├── __init__.py
│   │   │   └── installer.py
│   │   ├── rpm/               ← RHEL/CentOS 전용 설치 로직
│   │   │   ├── __init__.py
│   │   │   └── installer.py
│   │   └── main.py            ← 에이전트 진입점 (FastAPI + 스케줄러)
│   │
│   ├── debian/                ← `.deb` 빌드용 메타디렉터리
│   │   ├── control
│   │   ├── compat
│   │   ├── rules
│   │   ├── changelog
│   │   └── source/
│   │       └── format
│   │
│   ├── rpm/                   ← `.rpm` 빌드용 스켈레톤
│   │   ├── SPECS/
│   │   │   └── nacfy-agent.spec
│   │   └── SOURCES/
│   │
│   ├── packaging/             ← 템플릿·초안 보관용
│   │   ├── debian/            ← debian/control 등 초안
│   │   └── rpm/               ← rpm spec 예제 등
│   │
│   ├── requirements.txt       ← Python 의존성 목록
│   ├── README.md              ← 에이전트 전용 설명서
│   └── install-agent.sh       ← 설치 스크립트 (옵션)
│
├── server/                    ← Nacfy 서버 애플리케이션
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   └── main.py
│   └── debian/
│
├── shared/                    ← agent ↔ server 공통 라이브러리
│   └── utils.py
│
├── docs/
│   └── architecture.md
│
├── debian/                    ← 전체 프로젝트 패키징 (선택)
│
├── rpm/                       ← 전체 프로젝트 패키징 (선택)
│
└── README.md                  ← 프로젝트 개요, 설치·개발 가이드


```


### AI

| 단계                            | 핵심 책임                                                   | 구현 힌트                                                                     |
| ----------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------- |
| ① **데이터 수집 & 정규화**            | 에이전트가 실시간 메트릭·로그·보안 이벤트를 수집해 **표준 스키마(JSON)** 로 서버에 업로드 | 기존 `jobs/sysinfo.py`, `log_uploader.py` → “policy-features” 컬럼 추가         |
| ② **정책 추론(Policy Inference)** | AI 모델이 “현재 상태 → 추천 변경사항” 출력                             | `shared/ai/predictor.py`<br>∙ 룰 기반 + 보강 학습(LLM + RAG) or 작은 GNN/Tree 모델   |
| ③ **검증 & 적용(Orchestrator)**   | 모델 결과를 *규칙 엔진*·승인 플로우로 통과시킨 뒤, 에이전트에 **PUSH 명령**        | FastAPI `/command` endpoint + policy-engine(OPA Rego 등)                   |
| ④ **설명 생성(Explain)**          | “왜 이런 변경을 권했는가?” → 자연어 요약                               | LLM prompt: *“Because CPU > 85 % for 5 min, model X voted … therefore …”* |



| #       | 실행 지점 (실제 코드 파일 예)                                        | 호출·처리 내용                                                 | 주요 IO (URI · JSON 예시)                                                                                                                                                              |
| ------- | --------------------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**   | **웹 브라우저**<br>`chat.tsx`                                  | 사용자가 입력 → POST 전송                                        | **POST** `/api/ai/chat`<br>`{ "prompt": "SSH 포트 22 막아줘" }`                                                                                                                         |
| **2**   | **Web API 서버** (Node)<br>`routes/chat.ts`                 | ① 세션/권한-토큰 확인<br>② AI 서비스 호출                             | **POST** `http://ml-service:8001/chat`<br>`{ prompt, userId, serverId }`                                                                                                           |
| **3 a** | **AI 서비스** (Python FastAPI)<br>`ml-service/main.py`       | ① 로그/메트릭 DB 조회 (최근 5 분)<br>② `policy_model.predict()` 호출 | 내부 함수 호출 → `predict(features) → { answer, actions[] }`                                                                                                                             |
| **3 b** | **AI 모델**<br>`shared/ai/policy_model.py`                  | LLM/ML 추론 → **행동 목록 + 해설** 생성                            | 반환 예시:<br>`json {<br> "answer": "...차단이 권장됩니다",<br> "actions":[{<br>   "type":"apply_firewall",<br>   "target":"agent-prod-01",<br>   "payload":{"port":22,"allow":false}<br>}]} ` |
| **4**   | **Web API 서버**                                            | ① 브라우저에 채팅 답변 *스트리밍* (SSE/WS)<br>② Action을 정책엔진으로 전달     | **POST** `/internal/policy/validate`                                                                                                                                               |
| **5**   | **정책 엔진** (OPA Rego 또는 Python 룰)<br>`policy/validator.py` | 조직 룰 체크 · 승인 필요 여부 판단                                    | 승인 OK → 200 `{"approved":true}`                                                                                                                                                    |
| **6**   | **Web API 서버**                                            | 승인된 Action → **에이전트**에 푸시                                | **POST** `http://agent-prod-01:9010/command`<br>`{ id:"cmd-123", type:"apply_firewall", payload:{...} }`                                                                           |
| **7**   | **Agent** (FastAPI) <br>`agent/src/command_router.py`     | ① payload 검증<br>② 로컬 쉘 실행 `iptables -A INPUT ...`        | 로컬 OS 명령 실행                                                                                                                                                                        |
| **8**   | **Agent → Web API**                                       | 실행 결과 리포트                                                | **PUT** `/agent/exec-result/cmd-123`<br>`{ status:"success", appliedAt:"2025-06-21T08:30:12Z" }`                                                                                   |
| **9**   | **Web API 서버**                                            | 브라우저에 “적용 완료” 이벤트 push                                   | SSE `event:status data:{…"success"...}`                                                                                                                                            |














src/
├── jobs/      ← 모든 리눅스 배포판에서 동일하게 쓰는 주기작업 코드
├── service/   ← 모든 환경에서 동일하게 쓰는 HTTP 클라이언트 코드
├── common/    ← OS-agnostic 공통 유틸
├── debian/    ← Debian/Ubuntu 전용 설치 로직
└── rpm/       ← RHEL/CentOS 전용 설치 로직


## 주요 기능 

| 기능                            | AI 적용 예시                                                                                                       |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------|
| 1. 리소스 사용량 모니터링       | 이번 주 CPU·메모리·디스크 등 지표를 AI에 입력해 이상치(스파이크)를 탐지하고, 임계치 조정 방안 추천                |
| 2. 서비스 상태 관리             | “nginx가 중단되었을 때” 로그와 상태 정보를 AI에 전달해 원인 분석 → “서비스 재시작” 스크립트 자동 생성               |
| 3. 프로세스·포트 감시           | “포트 22가 예기치 않게 열리거나 닫혔을 때” AI가 위험도 분류 → 차단 또는 방화벽 규칙 자동 업데이트 커맨드 제안        |
| 4. 로그 파일 이상 탐지          | 대용량 로그를 AI 분류기에 넣어 새로운 에러·경고 패턴을 자동 태깅 및 요약 보고                                      |
| 5. 파일 무결성 검사             | “sshd_config 해시 변경” 시 변경된 라인과 정상 라인을 AI가 비교·해석 → 비정상 변경 여부 및 복구 명령 제안           |
| 6. 패치·업데이트 자동화         | 최신 보안 공지를 AI에 학습시켜 “이 패키지를 즉시 업데이트해야 함” vs “나중에 업데이트 가능” 우선순위 분류           |
| 7. 사용자 계정·권한 관리         | 신규 SSH 로그인 실패 기록을 AI에 요약 전달 → “브루트포스 공격 의심” 판단 후 자동 차단 스크립트 생성                |
| 8. 네트워크 연결·방화벽 설정 검사 | 허용되지 않은 IP 접근 패턴을 AI로 학습 → 실시간 탐지 및 iptables/UFW 차단 룰 자동 생성                           |
| 9. 커스텀 스크립트·명령 실행    | 중앙 서버 명령(JSON)을 AI 프롬프트로 해석 → 어디에 어떻게 실행할지 플랜 생성 후 자동 실행                         |
| 10. 자체 헬스체크 HTTP 엔드포인트 | `/healthz` 메트릭을 AI로 실시간 분석 → “이상 징후 사전 경고” 또는 “리소스 증설 권고” 보고                          |





## AI 
| 기능                | AI 적용 예시                                                          |
| ----------------- | ----------------------------------------------------------------- |
| 1. 리소스 사용량 모니터링   | 모델에게 “이번 주 CPU, 메모리 데이터”를 넣어 이상치(스파이크)를 찾아내고, 임계치 조정안 추천          |
| 2. 서비스 상태 관리      | “nginx가 중단됐을 때” 로그·상태를 AI에 보내서 원인 분석 후 “서비스 재시작” 스크립트 자동 생성       |
| 3. 프로세스·포트 감시     | “포트 22가 예상치 못하게 닫혔거나 열렸을 때” AI가 위험도 분류 → 방화벽 룰 재설정 커맨드 제안         |
| 4. 로그 파일 이상 탐지    | 대용량 로그를 AI 분류기로 돌려 “ERROR/WARNING 패턴” 이력 없이 새로운 에러 시그니처 자동 태깅     |
| 5. 파일 무결성 검사      | “sshd\_config 해시가 변했을 때” AI에게 변경된 라인과 정상 라인을 비교·해석 → 비정상 변경 여부 보고 |
| 6. 패치·업데이트 자동화    | 최신 보안 공지를 AI에 넣어 “이 패키지를 반드시 업데이트” vs “나중에 해도 됨” 우선순위 분류          |
| 7. 사용자 계정·권한 관리   | “새 SSH 로그인 실패 기록”을 AI에게 요약시켜 “브루트 포스 공격 의심” 판단 → 자동 차단 스크립트 생성    |
| 8. 네트워크 연결·방화벽 검사 | “비허용 IP 접근 시그니처”를 AI로 학습시켜 실시간 탐지·차단 룰(iptables/UFW) 자동 생성        |
| 9. 커스텀 스크립트 실행    | 중앙 명령(JSON)을 AI 프롬프트로 받아 “어디에 어떻게 실행해야 할지” 분석 후 실행 플랜 생성          |
| 10. 자체 헬스체크 엔드포인트 | `/healthz`에 수집된 메트릭을 AI로 실시간 예측 분석 → “이상 발생 전 경고” 또는 “리소스 증설” 제안  |




## PPA

테스트 배포 준비중







