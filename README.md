# 🐾 PawHealth Pro - Ultimate Veterinary Management System

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-latest-red.svg)
![uv](https://img.shields.io/badge/managed%20by-uv-purple.svg)

**PawHealth Pro** is an enterprise-grade backend microservice designed for comprehensive pet healthcare management. It features a **Smart Intelligence Engine** that aggregates clinical data, nutrition, and weight trends into a unified proactive care system.

---

## 🌟 Key Features

* **🧠 Unified Activity Timeline:** A sophisticated chronological engine that merges medical, feeding, and weight data into a single intelligence feed.
* **📸 Profile Media Management:** Secure image upload and static serving for pet profile pictures with file-type validation.
* **🏥 Clinical Medical Records:** Detailed tracking of veterinary visits inclu* **🏥 Clinical Medicio* **🏥 Clinical Medical Records:** Detailed tracking ocy SOS* **🏥 Clinical Medical Records:** Detailed tracking of veat* **🏥 Clinical Medical Records:** Detailed tracking of veterinary visits inclu* **🏥 Clin u* **🏥 Clinical Medical Records:** Detailed tracking of veterion* **🏥 Clinical Medical Records:** Detailed tracking of vIntegrated middleware logging request duration for high-traffic environment monitoring.

---

## 🏗 System Architecture

The project follows a modular architecture inspired by scalable microservices, focusing on separation of concerns and data persistence.

```text
ppppppppppppppp
├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├  �├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─�├─� seed.py          # Automated Database Seeding (Bonus)
├── tests/
│   ├── test_main.py     # Comprehensive Pytest Suite
│   └── __init__.py
├── uploads/             # Persistent Profile Image Storage
├── pyproject.toml       # Dependency & Environment Configuration
└── README.md            # Technical Documentation
🛠 Tech Stack
Language: Python 3.12+ (Typed)

Web Framework: FastAPI (Asynchronous logic)

ORM: SQLModel (Modern SQLAlchemy + Pydantic wrapper)

Package Manager: uv (High-performance dependency resolution)

Testing: Pytest with FastAPI TestClient

🚦 Getting Started
Initialize Environment
uv sync
Populate Demo Data (Bonus)
PYTHONPATH=. uv run python scripts/seed.py
Launch the API
uv run uvicorn app.main:app --reload
Execute Test Suite
uv run pytest
Interactive Documentation: Once the server is running, access the full Swagger UI at: http://127.0.0.1:8000/docs

📝 Design Philosophy
Developed as part of the EASS-HIT course, this project demonstrates advanced concepts in RESTful API design, database normalization, and automated business logic.

Created by Bar Aizenberg - Passionate about Dog Health & Software Engineering.

🤖 AI Assistance
This project was developed in collaboration with Gemini (Google). AI assisted in:

Designing the relational database architecture and SQLModel relationship logic.

Implementing the Unified Timeline aggregation and sorting algorithms.

Configuring the Pytest suite for robust validation and error-code verification.

All AI-generated components were manually reviewed, refactored, and verified through automated tests.
