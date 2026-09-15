import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


def web_search(query: str) -> str:
    """
    Search the web using Tavily and return relevant results.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return (
            "Web search is unavailable because TAVILY_API_KEY "
            "is not configured."
        )

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5,
    )

    results = response.get("results", [])

    if not results:
        return "No relevant web search results were found."

    formatted_results = []

    for result in results:
        title = result.get("title", "Untitled")
        content = result.get("content", "")
        url = result.get("url", "")

        formatted_results.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"Source: {url}"
        )

    return "\n\n---\n\n".join(formatted_results)