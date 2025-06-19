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
