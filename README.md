# NACFY

**NACFY** is a self-hosted network access control and monitoring platform.  
It provides centralized configuration management and agent communication for secure server environments.

## 📦 Project Structure
```
nacfy/
├── agent/                        # 서버에 설치되는 에이전트
│   ├── src/
│   │   └── agent.py             # 에이전트 메인 스크립트
│   └── requirements.txt         # 의존성 목록
│   └── venv/                    # (로컬) 가상환경
│
├── server/                      # nacfy 중앙 제어 서버
│   ├── src/
│   │   ├── controllers/         # API 로직 분리 예정
│   │   ├── routes/              # 라우트 분리 예정
│   │   └── index.js             # 서버 엔트리포인트
│   ├── web/                     # React UI
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   ├── public/
│   │   ├── index.html
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── package.json             # Express 서버용
│   └── .env                     # 서버 설정
│
├── shared/                      # 공통 상수/유틸 (선택)
├── docs/                        # 설계 문서, API 흐름도 등
├── .gitignore
├── README.md
└── docker-compose.yml           # (선택) 개발용 통합 실행 스크립트

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
