# 🐾 PawHealth Pro - Ultimate Veterinary Management (V3.6.1)

PawHealth Pro is an enterprise-grade backend solution for comprehensive pet healthcare. It features a Smart Intelligence Engine that monitors nutrition, weight trends, and medical schedules.

## 🌟 Pro Features
- **🧠 Unified Activity Timeline:** Chronological feed of medical, feeding, and weight events.
- **📸 Media Management:** Full support for profile picture uploads and static serving.
- **🏥 Clinical Medical Records:** Detailed tracking of vet visits including summaries and diagnoses.
- **🚨 Emergency SOS Registry:** Instant access to emergency contacts and chip IDs.
- **🛡️ Data Integrity:** Strict relational mapping and Pydantic validation (Weight > 0).

## 🏗 System Architecture
\`\`\`text
paw-health-api/
├── app/
│   ├── main.py          # API Engine & Routes
│   ├── models.py        # Relational SQLModel Schemas
│   ├── database.py      # Persistence Layer (SQLite)
├── scripts/
│   ├── seed.py          # Automated Demo Data (Bonus)
├── tests/
│   ├── test_main.py     # Pytest Suite
├── uploads/             # Image Storage
└── README.md            # Documentation
\`\`\`

## 🚦 Getting Started
1. **Initialize Environment:** \`uv sync\`
2. **Seed Demo Data (Bonus):** \`PYTHONPATH=. uv run python scripts/seed.py\`
3. **Launch System:** \`uv run uvicorn app.main:app --reload\`
4. **Run Tests:** \`uv run pytest\`

## 🤖 AI Assistance
This project was developed in collaboration with Gemini (Google). AI assisted in:
- Designing the relational architecture and SQLModel relationships.
- Implementing the Unified Timeline sorting logic.
- Configuring the Pytest suite for robust validation checking.
*All outputs were manually reviewed, integrated, and verified.*

**Created by Bar Aizenberg - Passionate about Dog Health & Software Engineering.**
