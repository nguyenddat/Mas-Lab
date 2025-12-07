from typing import Dict, Any, List

import arxiv
import requests

from core import config

def search_arxiv_papers_by_query(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Tool for searching papers on Arxiv by query.
    Args:
        query: str
        max_results: int
    Returns:
        List[{"arxiv_id": str, "title": str, "abstract": str, "authors": list[str], "download_url": str}]
    """
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

    papers = []
    for result in search.results():
        papers.append({
            "arxiv_id": result.entry_id.split('/')[-1],
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "download_url": result.pdf_url,
        })
    return papers

def create_paper(paper_in: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool for creating paper in database.
    Args:
        paper_in: {{
            "arxiv_id": str,
            "title": str,
            "abstract": str,
            "authors": list[str],
            "download_url": str,
        }}
    
    Outputs: List[{{
        "arxiv_id": str,
        "title": str,
        "abstract": str,
        "authors": list[str],
        "download_url": str,
        "pdf_url": str,
    }}]
    """
    api_url = f"{config.BACKEND_API_URL}/paper/"
    response = requests.post(api_url, json=paper_in)
    response.raise_for_status()
    return response.json()
