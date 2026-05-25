"""Web search tool.

By default this is a stub that returns a placeholder message.
To enable real search, set SEARCH_API_KEY in your .env and uncomment
the implementation that uses your preferred provider (e.g. SerpAPI, Tavily).
"""

import os

WEB_SEARCH_SCHEMA = {
    "name": "web_search",
    "description": "Search the web for up-to-date information on a topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string.",
            }
        },
        "required": ["query"],
    },
}


def web_search(query: str) -> str:
    """Perform a web search and return results as a string."""
    api_key = os.getenv("SEARCH_API_KEY")
    if not api_key:
        return (
            f"[web_search stub] No SEARCH_API_KEY found. "
            f"Would have searched for: '{query}'. "
            "Set SEARCH_API_KEY in .env to enable real search."
        )

    # Example: Tavily integration (pip install tavily-python)
    # from tavily import TavilyClient
    # client = TavilyClient(api_key=api_key)
    # results = client.search(query, max_results=5)
    # return "\n".join(r["content"] for r in results.get("results", []))

    return f"[web_search] Search for '{query}' not implemented. Add your provider above."
