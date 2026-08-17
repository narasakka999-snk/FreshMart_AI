import os
import requests
from dotenv import load_dotenv

load_dotenv()


def research_web(query, max_results=6):
    """
    Uses Tavily when TAVILY_API_KEY is configured.
    The application deliberately does not invent external evidence.
    """

    key = os.getenv("TAVILY_API_KEY")

    if not key:
        return [{
            "title": "Research service not configured",
            "summary": "Set TAVILY_API_KEY to enable live external research. No external evidence is fabricated by this application.",
            "url": ""
        }]

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": False
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return [
        {
            "title": r.get("title", ""),
            "summary": r.get("content", ""),
            "url": r.get("url", "")
        }
        for r in data.get("results", [])
    ] 
    