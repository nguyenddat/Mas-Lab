from pydantic import BaseModel

class PaperCreateRequest(BaseModel):
    arxiv_id: str
    title: str
    abstract: str
    authors: list[str]
    download_url: str