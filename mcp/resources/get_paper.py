import requests

from core import config

def get_paper_by_pdf_url(pdf_url: str) -> bytes:
    """
    Paper resource: read pdf content from backend by pdf_url.
    
    Args:
        pdf_url (str): file PDF in backend /papers/static/
    
    Returns:
        bytes: pdf content
    """
    api_url = f"{config.BACKEND_API_URL}/papers/static/{pdf_url}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.content