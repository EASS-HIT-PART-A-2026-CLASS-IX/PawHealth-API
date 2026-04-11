# 🐾 PawHealth Pro - V3.2.0

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)

Backend solution for pet healthcare with relational data tracking.

## 🚀 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/dogs` | List all dogs (with pagination) |
| **POST** | `/dogs` | Register a new dog |
| **DELETE** | `/dogs/{id}` | Remove a dog profile |
| **POST** | `/health/weight` | Log weight for a specific dog_id |
| **GET** | `/dogs/{id}/weight` | Get weight history for a dog |
| **POST** | `/health/feeding` | Log feeding session |
| **GET** | `/health` | System health check |

## 🏗 System Architecture
\`\`\`text
paw-health-api/
├── app/
│   ├── main.py          # CRUD & Pagination Logic
│   ├── models.py        # Relational Schemas (Foreign Keys)
│   ├── database.py      # SQLite Connection
└── README.md
\`\`\`

## 🤖 AI Assistance
This project uses Gemini (Google) for architectural design and relational schema validation. Verified via Pytest.

---
**Created by Bar Aizenberg**
