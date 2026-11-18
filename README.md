# 🤖 Financial Research Agent AI

An AI-powered financial research backend that gathers company information from web sources, analyzes financial data and business developments, and generates structured research briefs using LLM reasoning and tool orchestration.

Built with FastAPI, Tavily, Groq, and Cloudflare R2, the application demonstrates multi-step AI research, web content extraction, structured report generation, and cloud-based document storage.

## ⚡ What This System Does

- 🔍 Accepts a company name as input.
- 🌐 Searches the web for company information, financial data, news, and risks using Tavily.
- 📰 Extracts relevant content from selected web sources using BeautifulSoup and httpx.
- 🧠 Analyzes gathered information using Groq (LLaMA 3.3 70B).
- 📊 Generates a structured company research brief.
- 📄 Produces a formatted PDF research report using ReportLab.
- ☁️ Uploads generated reports to private Cloudflare R2 storage.
- 🗄️ Persists research metadata in Supabase PostgreSQL.
- 📥 Generates temporary download URLs for stored reports.

## 🧠 Agent Architecture

```text
User Input: Company Name
        ↓
Tavily Web Search
        ↓
Financial Overview Research
        ↓
Latest News Research
        ↓
Risks & Challenges Research
        ↓
Web Content Extraction
(BeautifulSoup + httpx)
        ↓
LLM Analysis
(Groq LLaMA 3.3 70B)
        ↓
Structured Research Brief
        ↓
PDF Report Generation
(ReportLab)
        ↓
Cloud Storage
(Cloudflare R2)
        ↓
Metadata Persistence
(Supabase PostgreSQL)
        ↓
JSON API Response
(Research Insights + Download URL)
```

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| LLM | Groq (LLaMA 3.3 70B) |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup + httpx |
| Report Generation | ReportLab |
| Object Storage | Cloudflare R2 |
| Database | Supabase PostgreSQL + SQLModel |
| Containerization | Docker |
| Deployment | Render |
| Dependency Management | Poetry |

## 🏗️ Project Structure

```text
financial-research-agent/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   │       └── research.py
│   ├── agent/
│   │   ├── researcher.py
│   │   └── tools.py
│   ├── services/
│   │   ├── report_service.py
│   │   └── storage_service.py
│   ├── db/
│   │   └── database.py
│   └── models/
│       └── research.py
├── Dockerfile
├── .dockerignore
├── .env.example
├── pyproject.toml
└── poetry.lock
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Poetry
- [Groq](https://console.groq.com) API key
- [Tavily](https://tavily.com) API key
- [Supabase](https://supabase.com) PostgreSQL project
- [Cloudflare R2](https://developers.cloudflare.com/r2/) bucket

### 1. Clone the repository

```bash
git clone https://github.com/Abdullateef1x/financial-research-agent-ai
cd financial-research-agent
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Configure environment variables

Create your local environment file:

```bash
cp .env.example .env
```

Configure the required variables:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

DATABASE_URL=your_supabase_postgresql_connection_string

R2_ACCOUNT_ID=your_cloudflare_account_id
R2_ACCESS_KEY_ID=your_r2_access_key
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=your_bucket_name
```

Keep `.env` private. Never commit API keys, database credentials, or storage secrets to Git.

### 4. Run locally

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 5. Run with Docker

```bash
docker build -t financial-research-agent .
docker run -p 8000:8000 financial-research-agent
```

Configure the required environment variables when running the container.

## 📡 API Endpoints

### `POST /research`

Runs the research workflow for a supplied company name.

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Apple Inc"}'
```

Example response:

```json
{
  "report_id": "3EB75B71",
  "company": "Apple Inc",
  "ticker": "AAPL",
  "sector": "Technology",
  "recommendation": "Hold",
  "confidence": 0.8,
  "summary": "Company research summary...",
  "report_url": "<temporary-presigned-download-url>",
  "created_at": "2026-11-18T10:30:00"
}
```

The response fields above illustrate the API structure; actual research results depend on the retrieved sources and model output.

### `GET /reports`

Retrieves previously generated research reports.

```bash
curl http://localhost:8000/reports
```

Returns report metadata and freshly generated download URLs.

### `GET /health`

Checks API health.

```bash
curl http://localhost:8000/health
```

## 📦 Report Storage

Generated PDF reports are stored in private Cloudflare R2 object storage.

The application stores R2 object keys in the database rather than relying on expiring download URLs.

When a report is requested:

1. The API retrieves the report's stored object key.
2. The storage service generates a fresh presigned download URL.
3. The API returns the URL to the client.

Presigned download URLs expire after **one hour**.

This allows reports to remain stored independently of individual download links.

## 📊 Research Brief Contents

Each generated PDF research report can include:

| Section | Details |
|---|---|
| Business Overview | Company description and business activities |
| Key Financials | Revenue, net income, market capitalization, P/E ratio, and growth where available |
| Strengths | Identified competitive advantages |
| Risks | Potential business and financial risks |
| Recent News | Relevant headlines and their assessed impact |
| Competitive Position | Company positioning and market context |
| Research Assessment | LLM-generated analysis and recommendation rationale |
| Data Sources | Sources used during research |

Financial information depends on the availability and reliability of retrieved sources. Missing or unavailable figures should not be interpreted as zero.

## 🧪 Example Research Requests

The API accepts company names as input. Example research targets include:

**Technology**
- Apple
- Microsoft
- NVIDIA

**Nigerian and African businesses**
- Dangote Cement
- MTN Nigeria
- Flutterwave

**Financial Services**
- JPMorgan Chase
- Goldman Sachs

These are examples of research inputs, not endorsements or investment recommendations.

## 🧠 Skills Demonstrated

- Agentic AI application development
- LLM integration and orchestration
- Multi-step research workflows
- Web search integration using Tavily
- Web content extraction using BeautifulSoup and httpx
- Structured LLM outputs
- FastAPI backend engineering
- PDF report generation
- Cloud object storage integration
- Relational database persistence
- Logging and application observability
- Docker-based application packaging

## ⚠️ Research Limitations and Disclaimer

This application generates AI-assisted company research based on information retrieved from external sources.

- Retrieved information may be incomplete, outdated, or inaccurate.
- Web scraping depends on source availability and website structure.
- LLM-generated analysis may contain errors or unsupported conclusions.
- Financial metrics should be independently verified against reliable financial disclosures.

Reports are for informational and educational purposes only. They are not financial advice or a substitute for independent research and professional judgment.

## 📄 License

[Add your chosen license here.]