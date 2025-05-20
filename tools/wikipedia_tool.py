from langchain_core.tools import tool
import wikipedia

@tool
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia and returns a summary of the topic."""
    try:
        return wikipedia.page(query)
    except Exception as e:
        return f"Error fetching Wikipedia summary: {str(e)}"
