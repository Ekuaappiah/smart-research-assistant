import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

@tool
def get_tavily(name: str):
    """
    Searches Tavily for the top 3 results matching the given name query.
    """
    search = TavilySearchResults(max_results=5, api_key=tavily_api_key)
    res = search.run(f"{name}")
    return res
