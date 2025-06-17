# NACFY

**NACFY** is a self-hosted network access control and monitoring platform.  
It provides centralized configuration management and agent communication for secure server environments.

## 📦 Project Structure

nacfy/
├── server/ # nacfy 중앙 제어 서버
│ ├── src/
│ │ ├── controllers/
│ │ ├── routes/
│ │ ├── models/
│ │ └── index.js
│ └── package.json
├── agent/ # 서버에 설치되는 에이전트
│ ├── src/
│ │ ├── tasks/
│ │ └── agent.py
│ └── requirements.txt
├── shared/ # 공통 상수/유틸 (선택)
├── docs/ # 설계 문서, API 흐름도
├── .env
├── .gitignore
├── README.md
└── docker-compose.yml # (선택) 개발용 통합 실행 스크립트