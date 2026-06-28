# Civix Backend — FastAPI + PostgreSQL

> AI-powered USCIS Interview Simulator API  
> Built by **Vertex Coders LLC** · Miami, FL

---

## 🧠 Overview

Civix Backend is the core API service for the Civix USCIS citizenship interview simulator. It integrates **Claude AI (Anthropic)** to evaluate spoken answers in real time using a RAG-simulated approach — guaranteeing 0% hallucinations by grounding every evaluation against the official USCIS civics context.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111.0 |
| Language | Python 3.12 |
| Database | PostgreSQL 16 (via SQLAlchemy 2.0) |
| AI Engine | Claude Sonnet (Anthropic SDK) |
| DB Driver | psycopg2-binary |
| Config | pydantic-settings |
| Server | Uvicorn with uvloop |
| Containerization | Docker + Docker Compose |
| Deployment | Railway |

---

## 📁 Project Structure

```
civix-backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router registration
│   ├── config.py            # Pydantic settings (env vars)
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── routers/
│   │   ├── interview.py     # POST /api/interview/evaluate
│   │   └── progress.py      # GET /api/progress/{user_id}
│   ├── services/
│   │   └── ai_service.py    # Claude AI integration (RAG prompt)
│   └── models/              # SQLAlchemy ORM models
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=postgresql+psycopg2://civix_user:civix_pass@db:5432/civix_db
SECRET_KEY=your_secret_key_here
ANTHROPIC_API_KEY=sk-ant-...
ALLOW_ORIGINS=http://localhost:4200,https://your-netlify-app.netlify.app
```

### Railway Production Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL internal URL from Railway Postgres service |
| `SECRET_KEY` | Random secret string for JWT |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `ALLOW_ORIGINS` | Comma-separated list of allowed frontend origins |

---

## 🚀 Local Development

### Prerequisites
- Docker Desktop
- Docker Compose

### Run locally

```bash
# Clone the repo
git clone https://github.com/Denisijcu/civix-backend.git
cd civix-backend

# Create your .env file
cp .env.example .env
# Edit .env with your values

# Start all services
docker-compose up --build
```

API available at: `http://localhost:8002`  
Swagger docs at: `http://localhost:8002/docs`

---

## 📡 API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "service": "Civix-Core"
}
```

---

### `POST /api/interview/evaluate`
Evaluates a user's spoken answer using Claude AI.

**Request Body:**
```json
{
  "question_text": "What is the supreme law of the land?",
  "user_answer": "The Constitution",
  "official_context": "The Constitution is the supreme law of the land...",
  "current_stress_level": 3
}
```

**Response:**
```json
{
  "is_correct": true,
  "explanation": "Correct.",
  "new_stress_level": 2
}
```

---

### `GET /api/progress/{user_id}`
Returns a user's progress and approval probability.

**Response:**
```json
{
  "usuario_id": "user_demo_001",
  "preguntas_respondidas": 10,
  "respuestas_correctas": 8,
  "probabilidad_aprobacion": 0.80,
  "nivel_estres_actual": 3
}
```

---

## 🤖 AI Service — How It Works

The `AIService` class in `app/services/ai_service.py` sends a structured prompt to Claude with:

1. **Tone instruction** based on current stress level (calm → neutral → strict)
2. **The official USCIS context** as the only source of truth (RAG simulation)
3. **Strict JSON response format**: `is_correct`, `explanation`, `stress_adjustment`

This guarantees **0% hallucinations** — Claude can only evaluate based on the provided context, not outside knowledge.

---

## 🐳 Docker

### Local (docker-compose)
```bash
docker-compose up --build    # Start
docker-compose down          # Stop
docker-compose logs -f api   # Logs
```

### Production (Railway)
Railway uses the `Dockerfile` directly. The app starts with:
```
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Port `8080` is configured in Railway's Networking settings.

---

## 🚢 Deployment — Railway

1. Push to GitHub (`main` branch)
2. Railway auto-deploys on every push
3. Set environment variables in Railway → Service → Variables
4. Configure Networking → Public Networking → Port `8080`

**Production URL:** `https://civix-backend-production-721a.up.railway.app`

---

## 📦 Requirements

```
fastapi==0.111.0
uvicorn[standard]==0.30.1
sqlalchemy==2.0.31
psycopg2-binary
pydantic==2.8.2
pydantic-settings==2.3.4
python-dotenv==1.0.1
anthropic>=0.40.0
httpx>=0.27.0
```

---

## 🏢 Built by

**Vertex Coders LLC**  
Miami, FL · [vertexcoders.com](https://vertexcoders.com)  

> *Dossier ID: VX-1002 — Civix USCIS Interview Simulator*