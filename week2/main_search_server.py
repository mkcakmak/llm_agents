from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv() # TAVILY_API_KEY comes from .env

mcp = FastMCP("Search")


@mcp.prompt()
def general_question_prompt(topic:str,tone:str) ->str:
    """Generic template for asking about any topic in a specific tone."""
    return f"Please answer the following question in a {tone} tone : {topic}"


@mcp.tool()
async def search_internet(query:str) ->str:
    """
    Use web search to find accurate, up to date information.

    Args:
        query : The search query / question to look up on the web
    """

    search = TavilySearch(
        max_results=5,
        topic = "general",
    )

    # NOTE: must actually invoke the search and return its result,
    # not the TavilySearch tool object itself.

    result = await search.ainvoke({"query": query})
    print(f"[MCP Search Server] Web Search for : {query}")
    return str(result)

if __name__ == "__main__":
    # stdio transport: client starts this as a subprocess.
    mcp.run(transport="stdio")
