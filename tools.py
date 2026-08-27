'''
from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
        '''

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set in environment or .env file.")
    return TavilyClient(api_key=api_key)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    try:
        tavily = get_tavily_client()
        results = tavily.search(query=query, max_results=5)
        out = []
        for r in results.get("results", []):
            out.append(
                f"Title: {r.get('title', 'N/A')}\n"
                f"URL: {r.get('url', 'N/A')}\n"
                f"Snippet: {r.get('content', '')[:350]}\n"
            )
        return "\n----\n".join(out) if out else "No search results found."
    except Exception as e:
        return f"Web search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deep technical reading."""
    if not url or not url.startswith("http"):
        return f"Invalid URL provided: {url}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(url, timeout=10, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
                tag.decompose()
            cleaned_text = soup.get_text(separator=" ", strip=True)
            if len(cleaned_text) > 100:
                return cleaned_text[:5000]
    except Exception:
        pass

    # Fallback to Tavily Extract API if direct requests fails or gets blocked
    try:
        tavily = get_tavily_client()
        extracted = tavily.extract(urls=[url])
        results = extracted.get("results", [])
        if results and results[0].get("raw_content"):
            return results[0]["raw_content"][:5000]
    except Exception as e:
        return f"Could not scrape URL {url}: {str(e)}"

    return f"Unable to extract meaningful content from {url}."
