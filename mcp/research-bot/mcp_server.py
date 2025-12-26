from mcp.server.fastmcp import FastMCP
from src.tools import search_arxiv, get_paper_info

mcp_server = FastMCP("Research Bot MCP Server")

@mcp_server.tool()
def search_arxiv(query: str, max_results: int = 5) -> list[str]:
    """
    Search for papers on arXiv based on a query string and store the results in a specified path.
    
    Args:
        query (str): The search query string.
        max_results (int): The maximum number of results to return.
        
    Returns:
        List of arxiv Paper IDs for the found papers.
    """
    return search_arxiv(query, max_results)

@mcp_server.tool()
def get_paper_info(paper_id: str) -> dict:
    """
    Retrieve information about a specific paper by its arXiv ID.
    
    Args:
        paper_id (str): The arXiv ID of the paper.
        
    Returns:
        dict: A dictionary containing the paper's information.
    """
    return get_paper_info(paper_id)

if __name__ == "__main__":
    mcp_server.run(transport="stdio")
    