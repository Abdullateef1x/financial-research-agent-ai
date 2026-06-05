# 🤖 Financial Research Agent AI

An AI-powered financial research agent that autonomously searches the web, scrapes financial data, and generates structured investment briefs using LLM reasoning and agentic tool use.

Built as a production-ready AI agent system demonstrating autonomous web research, multi-step reasoning, and structured report generation.

---

## ⚡ What This System Does

- 🔍 Takes a company name as input
- 🌐 Autonomously searches the web for financial data, news, and risks (Tavily)
- 📰 Scrapes top financial sources for deeper content
- 🧠 Reasons over gathered data using LLM (Groq LLaMA 3.3 70B)
- 📊 Generates a structured investment brief (Buy / Hold / Sell)
- 📄 Produces a formatted PDF research report (ReportLab)
- ☁️ Uploads report to Cloudflare R2
- 🗄️ Saves metadata to Supabase

---

## 🧠 Agent Architecture

```
User Input: Company Name
        ↓
Tavily Web Search (Financial Overview)
        ↓
Tavily Web Search (Latest News)
        ↓
Tavily Web Search (Risks & Challenges)
        ↓
BeautifulSoup Scraping (Top URLs)
        ↓
LLM Reasoning — Groq LLaMA 3.3 70B
        ↓
Structured Investment Brief (JSON)
        ↓
PDF Report Generation (ReportLab)
        ↓
Cloud Storage (Cloudflare R2 + Supabase)
        ↓
JSON API Response (Report URL + Insights)
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| LLM Engine | Groq (LLaMA 3.3 70B) |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup + httpx |
| Report Generation | ReportLab |
| File Storage | Cloudflare R2 |
| Database | Supabase (PostgreSQL) + SQLModel |
| Containerization | Docker |
| Deployment | Render |
| Dependency Management | Poetry |

---

## 🏗️ Project Structure

```
financial-research-agent/
├── app/
│   ├── main.py                    # App entry point, route registration, CORS
│   ├── api/
│   │   └── routes/
│   │       └── research.py        # /research, /reports endpoints
│   ├── agent/
│   │   ├── researcher.py          # Core agent loop — search, scrape, reason
│   │   └── tools.py               # Tavily search + BeautifulSoup scraping tools
│   ├── services/
│   │   ├── report_service.py      # ReportLab PDF investment brief generation
│   │   └── storage_service.py     # Cloudflare R2 upload
│   ├── db/
│   │   └── database.py            # SQLModel engine + session
│   └── models/
│       └── research.py            # ResearchReport SQLModel table
├── Dockerfile
├── .dockerignore
├── .env.example
├── pyproject.toml
└── poetry.lock
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Poetry
- [Groq](https://console.groq.com) API key
- [Tavily](https://tavily.com) API key
- [Supabase](https://supabase.com) project
- [Cloudflare R2](https://cloudflare.com) bucket

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/financial-research-agent.git
cd financial-research-agent
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key_id
R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com/your_bucket
```

### 4. Run locally

```bash
poetry run uvicorn app.main:app --reload
```

### 5. Run with Docker

```bash
docker compose up --build
```

---

## 📡 API Endpoints

### `POST /research`
Run the full research agent pipeline for a company. Returns structured investment brief and PDF report URL.

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Apple Inc"}'
```

**Response:**
```json
{
  "report_id": "3EB75B71",
  "company": "Apple Inc",
  "ticker": "AAPL",
  "sector": "Technology",
  "recommendation": "Buy",
  "confidence": 0.8,
  "summary": "Apple Inc is a technology company...",
  "report_url": "https://your-bucket.r2.cloudflarestorage.com/research/research_3EB75B71_Apple_Inc.pdf",
  "created_at": "2026-06-04T21:33:46.265470"
}
```

---

### `GET /reports`
List all previously generated research reports.

```bash
curl http://localhost:8000/reports
```

**Response:**
```json
{
  "total": 5,
  "reports": [
    {
      "report_id": "3EB75B71",
      "company": "Apple Inc",
      "ticker": "AAPL",
      "sector": "Technology",
      "recommendation": "Buy",
      "confidence": 0.8,
      "created_at": "2026-06-04T21:33:46.265470",
      "report_url": "https://..."
    }
  ]
}
```

---

### `GET /health`
Health check.

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## 📊 Investment Brief Report

Each generated PDF report contains:

| Section | Details |
|---|---|
| Recommendation Banner | Buy / Hold / Sell with confidence score |
| Business Overview | Company description and revenue drivers |
| Key Financials | Revenue, net income, market cap, P/E ratio, growth |
| Strengths | Key competitive advantages |
| Risks | Major risk factors |
| Recent News | Headlines with positive / negative / neutral impact |
| Competitive Position | Market position analysis |
| Recommendation Rationale | LLM reasoning behind the recommendation |
| Data Sources | Sources used for the analysis |

---

## 🧪 Example Companies to Research

```bash
# Large cap tech
{"company_name": "Apple Inc"}
{"company_name": "Microsoft"}
{"company_name": "NVIDIA"}

# Nigerian/African companies
{"company_name": "Dangote Cement"}
{"company_name": "MTN Nigeria"}
{"company_name": "Flutterwave"}

# Finance
{"company_name": "JPMorgan Chase"}
{"company_name": "Goldman Sachs"}
```

---

## 🧠 Skills Demonstrated

- Agentic AI system design
- LLM tool use and orchestration (Groq / LLaMA 3.3 70B)
- Autonomous web research (Tavily)
- Web scraping and content extraction (BeautifulSoup)
- Structured LLM outputs with JSON mode
- FastAPI backend engineering
- PDF report generation (ReportLab)
- Cloud storage integration (Cloudflare R2)
- Relational database persistence (Supabase + SQLModel)
- Containerization (Docker)
- Production deployment (Render)

---

## 🌍 Why This Project Matters

Demonstrates production-level agentic AI engineering skills relevant to:

- AI Engineer roles
- LLM Application Engineer positions
- Backend Engineer (AI Systems)
- AI Full-Stack Engineer positions

---

## ⚠️ Disclaimer

Reports generated by this system are for informational purposes only and do not constitute financial advice. Always conduct your own due diligence before making investment decisions.

---

## 📄 License

MIT