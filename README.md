# FactCheck AI API

A production-style REST API that combines **pharmacy claims management** with **AI-powered fact-checking** using the Gemini LLM API. Built with **Python 3.12** and **Flask 3**.

---

## Features

- Pharmacy claims CRUD with automated fraud detection
- AI fact-checking via Gemini API (with demo mode fallback)
- Batch fact-checking (up to 5 claims at once)
- Analytics endpoint with aggregated statistics
- OOP architecture with dataclasses, enums, and type hints
- 11 pytest unit/integration tests
- Docker support + GitHub Actions CI/CD

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Flask 3.0 |
| AI Integration | Google Gemini API |
| Testing | pytest, pytest-flask |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## Getting Started

```bash
git clone https://github.com/DianaM12-2/factcheck-ai-api.git
cd factcheck-ai-api
pip install -r requirements.txt

# Optional: add Gemini API key for real AI responses
echo "GEMINI_API_KEY=your_key_here" > .env

python run.py
```

API runs at `http://localhost:5000`

### Run with Docker
```bash
docker build -t factcheck-ai-api .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key factcheck-ai-api
```

### Run tests
```bash
pytest tests/ -v
```

---

## API Endpoints

### Claims
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/claims` | Get all claims |
| GET | `/api/v1/claims/<id>` | Get claim by ID |
| POST | `/api/v1/claims` | Create claim |
| DELETE | `/api/v1/claims/<id>` | Delete claim |
| GET | `/api/v1/claims/flagged` | Get flagged claims |
| GET | `/api/v1/claims/analytics` | Get analytics |

### Fact-Check
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/factcheck` | Check a single claim |
| POST | `/api/v1/factcheck/batch` | Check up to 5 claims |
| GET | `/health` | Health check |

---

## Example

```bash
# Fact check a claim
curl -X POST http://localhost:5000/api/v1/factcheck \
  -H "Content-Type: application/json" \
  -d '{"claim": "Aspirin is used to treat headaches."}'

# Response
{
  "verdict": "TRUE",
  "confidence": 0.95,
  "confidence_percent": "95.0%",
  "explanation": "Aspirin is widely used as an analgesic for headache relief.",
  "sources_consulted": 1
}
```

---

## Author

**Diana Martinez** — [GitHub](https://github.com/DianaM12-2) · [LinkedIn](https://linkedin.com/in/diana-martinez-s)
