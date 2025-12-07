from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .repo_base import BaseRepo
from models.model_paper import Paper
from core.logging import logger

class PaperRepo(BaseRepo):
    def __init__(self):
        super().__init__(Paper)
        
    # Create
    def create_paper(self, paper: Paper, db: Session) -> Paper:
        existing_paper = self.get_by_arxiv_id(paper.arxiv_id, db)
        if existing_paper:
            logger.warning(f"Paper with arxiv_id {paper.arxiv_id} already exists (found by check).")
            return existing_paper
            
        try:
            return self.create(paper, db)
        except IntegrityError:
            db.rollback()
            logger.warning(f"Paper with arxiv_id {paper.arxiv_id} already exists (found by constraint).")
            return self.get_by_arxiv_id(paper.arxiv_id, db)

    # Get
    def get_by_arxiv_id(self, arxiv_id: str, db: Session) -> Optional[Paper]:
        return db.query(Paper).filter(Paper.arxiv_id == arxiv_id).first()