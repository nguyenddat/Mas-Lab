from typing import Optional

from sqlalchemy.orm import Session

from models.model_paper import Paper
from repositories import paper_repo

class PaperService:
    @staticmethod
    def create_paper(paper: Paper, db: Session) -> Paper:
        return paper_repo.create_paper(paper, db)
    
    @staticmethod
    def get_by_arxiv_id(arxiv_id: str, db: Session) -> Optional[Paper]:
        return paper_repo.get_by_arxiv_id(arxiv_id, db)