import json
import os
from groq import Groq
from app.agent.tools import (
    search_company,
    search_company_news,
    search_company_risks,
    scrape_url,
)


def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_research_agent(company_name: str) -> dict:
    client = get_groq_client()

    # ── Step 1: Gather raw data from all three searches ──────
    print(f"[Agent] Searching financial overview for {company_name}...")
    financial_results = search_company(company_name)

    print(f"[Agent] Searching news for {company_name}...")
    news_results = search_company_news(company_name)

    print(f"[Agent] Searching risks for {company_name}...")
    risk_results = search_company_risks(company_name)

    # ── Step 2: Scrape top URLs for deeper content ───────────
    scraped_content = []
    for result in (financial_results + news_results)[:3]:
        url = result.get("url", "")
        if url:
            print(f"[Agent] Scraping {url}...")
            content = scrape_url(url)
            scraped_content.append(f"Source: {url}\n{content}")

    # ── Step 3: Build context for LLM ───────────────────────
    search_context = "\n\n".join([
        f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nContent: {r.get('content', '')}"
        for r in financial_results + news_results + risk_results
    ])

    scraped_context = "\n\n---\n\n".join(scraped_content)

    # ── Step 4: LLM generates structured investment brief ────
    print(f"[Agent] Generating investment brief for {company_name}...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a senior financial analyst. 
Analyze the provided research data and generate a structured investment brief.
Respond ONLY with a valid JSON object matching this exact structure:
{
  "company_name": string,
  "ticker": string or null,
  "sector": string or null,
  "headquarters": string or null,
  "founded": string or null,
  "business_overview": string (2-3 sentences),
  "key_financials": {
    "revenue": string or null,
    "net_income": string or null,
    "market_cap": string or null,
    "pe_ratio": string or null,
    "revenue_growth": string or null
  },
  "strengths": [string],
  "risks": [string],
  "recent_news": [{"headline": string, "impact": "positive" | "negative" | "neutral"}],
  "competitive_position": string (1-2 sentences),
  "recommendation": "Buy" | "Hold" | "Sell",
  "recommendation_rationale": string (2-3 sentences),
  "confidence": number (0.0 to 1.0),
  "data_sources": [string]
}
Base your analysis strictly on the provided data. If a field cannot be determined, use null."""
            },
            {
                "role": "user",
                "content": f"""Research data for {company_name}:

=== SEARCH RESULTS ===
{search_context}

=== SCRAPED CONTENT ===
{scraped_context}

Generate a comprehensive investment brief based on this data."""
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=2000,
    )

    raw = completion.choices[0].message.content
    if not raw:
        raise ValueError("LLM returned empty response")

    brief = json.loads(raw)
    if not isinstance(brief, dict):
        raise ValueError(f"Expected dict, got {type(brief)}")

    return brief