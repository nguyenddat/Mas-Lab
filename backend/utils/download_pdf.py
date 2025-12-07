import os
import requests
from urllib.parse import urlparse

from core import config

def download_pdf(pdf_url: str) -> str:
    parsed_url = urlparse(pdf_url)
    filename = os.path.basename(parsed_url.path)
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    file_path = os.path.join(config.PAPER_DIR, filename)
    
    response = requests.get(pdf_url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return filename, file_path