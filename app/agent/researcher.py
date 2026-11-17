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

    financial_response = search_company(company_name)
    financial_results = financial_response.get("results", [])
    financial_answer = financial_response.get("answer", "")

    print(f"[Agent] Searching news for {company_name}...")
    news_results = search_company_news(company_name)

    print(f"[Agent] Searching risks for {company_name}...")
    risk_results = search_company_risks(company_name)

    # ── Step 2: Scrape only 1 URL ───────────
    scraped_content = []
    for result in (financial_results)[:1]:
        url = result.get("url", "")
        if url and not url.endswith(".pdf"): # Skip PDFs for now
            print(f"[Agent] Scraping {url}...")
            content = scrape_url(url, max_chars=2000)

            if content.startswith("Could not scrape"):
                print("[Agent] Direct scraping unavailable; using Tavily search content.")
                continue

            scraped_content.append(f"Source: {url}\n{content}")

    # ── Step 3: Build context for LLM ───────────────────────
    top_results = (
        financial_results[:2]
        + news_results[:2]
        + risk_results[:2]
    )    
    search_context = "\n\n".join([
        f"Title: {r.get('title', '')}\n"
        f"URL: {r.get('url', '')}\n"
        f"Relevance Score: {r.get('score', '')}\n"
        f"Content: {r.get('content', '')[:1000]}"
        for r in top_results
    ])

    scraped_context = "\n\n".join(scraped_content) if scraped_content else "No scraped content."

    # ── Step 4: LLM generates structured investment brief ────
    print(f"[Agent] Generating investment brief for {company_name}...")
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
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

Base your analysis strictly on the provided data. If a field cannot be determined, use null.

For data_sources, include the exact URLs of the provided search results
that support your analysis. Never invent URLs or sources.
Do not treat Tavily's generated summary as an independent source.
Financial data rules:
- Never combine annual financial results with trailing twelve-month (TTM) figures.
- Never present projected or estimated figures as reported actuals.
- Preserve the exact financial reporting period and fiscal year for every figure.
- Do not assume calendar years and fiscal years are interchangeable.
- If sources disagree about a financial figure or reporting period, identify the discrepancy.
- If the reporting period or classification cannot be established, return null.
- Never calculate financial growth using figures from incompatible periods.
- If the supplied sources do not support a claim, do not present it as fact.
Investment recommendation rules:
- Do not issue a Buy or Sell recommendation based only on revenue growth or positive business performance.
- Consider valuation, profitability, financial performance, competitive position, and material risks.
- A P/E ratio must have a source and an identifiable as-of date.
- If valuation data or sufficient evidence is unavailable, use "Hold".
- Confidence must reflect the quality, completeness, and consistency of the evidence, not just how convincing the narrative sounds.
- Do not present an investment recommendation as certain.
"""
            },
            {
                "role": "user",
                "content": f"""Research data for {company_name}:

=== TAVILY FINANCIAL SUMMARY ===
{financial_answer}

=== SEARCH RESULTS ===
{search_context}

=== SCRAPED CONTENT ===
{scraped_context}

Generate a comprehensive investment brief based on this data."""
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=8000,
    )

    raw = completion.choices[0].message.content
    if not raw:
        raise ValueError("LLM returned empty response")

    brief = json.loads(raw)
    if not isinstance(brief, dict):
        raise ValueError(f"Expected dict, got {type(brief)}")

    brief["data_sources"] = list(dict.fromkeys(
        result["url"]
        for result in top_results
        if result.get("url")
    ))

    return brief