import os
import httpx
from bs4 import BeautifulSoup
from tavily import TavilyClient


def get_tavily_client():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_company(company_name: str) -> list[dict]:
    client = get_tavily_client()
    results = client.search(
        query=f"{company_name} financial overview revenue profit 2024 2025",
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )
    return results.get("results", [])


def search_company_news(company_name: str) -> list[dict]:
    client = get_tavily_client()
    results = client.search(
        query=f"{company_name} latest news earnings analyst outlook 2025",
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )
    return results.get("results", [])


def search_company_risks(company_name: str) -> list[dict]:
    client = get_tavily_client()
    results = client.search(
        query=f"{company_name} risks challenges competitors market position",
        search_depth="advanced",
        max_results=3,
        include_answer=True,
    )
    return results.get("results", [])


def scrape_url(url: str, max_chars: int =1500) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Return first max_chars characters to stay within LLM context
        return text[:max_chars]
    except Exception as e:
        return f"Could not scrape {url}: {e}"