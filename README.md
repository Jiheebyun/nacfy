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
