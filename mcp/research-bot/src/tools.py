import arxiv
import json
from typing import Optional
from src.config import papers_path, logger

storage_path = papers_path

def search_arxiv(query: str, max_results: int = 5) -> list[str]:
    """
    Search for papers on arXiv based on a query string and store the results in a specified path.
    
    Args:
        query (str): The search query string.
        max_results (int): The maximum number of results to return.
        
    Returns:
        List of arxiv Paper IDs for the found papers.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = client.results(search)
    logger.info(f"Found {max_results} papers for query: '{query}'")

    try:
        with open(storage_path, 'r') as f:
            papers_info = json.load(f)
            logger.info(f"Loaded existing papers info from {storage_path}")
    except (FileNotFoundError, json.JSONDecodeError):
        logger.info(f"No existing data found at {storage_path}. Initializing new storage.")
        papers_info = {}
        
    paper_ids = []
    for paper in papers:
        paper_id = str.split(paper.entry_id, '/')[-1]
        paper_ids.append(paper_id)
        if paper_id not in papers_info:
            papers_info[paper_id] = {
                'title': paper.title,
                'authors': [str(author) for author in paper.authors],
                'summary': paper.summary,
                'published': paper.published.isoformat(),
                'updated': paper.updated.isoformat(),
                'pdf_url': paper.pdf_url
            }
    
    with open(storage_path, 'w') as f:
        json.dump(papers_info, f, indent=2)
    logger.info(f"Stored paper information in {storage_path}")
    return paper_ids

def get_paper_info(paper_id: str) -> Optional[dict]:
    """
    Retrieve information about a specific paper by its arXiv ID.
    
    Args:
        paper_id (str): The arXiv ID of the paper.
        
    Returns:
        dict: A dictionary containing the paper's information.
    """
    try:
        with open(storage_path, 'r') as f:
            papers_info = json.load(f)
    except json.JSONDecodeError:
        logger.error(f"Data at {storage_path} is corrupted or not in valid JSON format.")
    except FileNotFoundError:
        logger.error(f"No valid storage found at {storage_path}.")
        return None
        
    if paper_id in papers_info:
        return papers_info[paper_id]
    else:
        logger.warning(f"===(get_paper_info)=== Paper ID {paper_id} not found in storage.")
        
arxiv_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_arxiv",
            "description": "Search for papers on arXiv based on a query string, store the results and get paper IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "The maximum number of results to return.",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_paper_info",
            "description": "Retrieve information about a specific paper by its arXiv ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "The arXiv ID of the paper."
                    }
                },
                "required": ["paper_id"]
            }
        }
    }
]
