from typing import Optional
from sqlalchemy.orm import Session

from .repo_base import BaseRepo
from models.model_paper import Paper

class PaperRepo(BaseRepo):
    def __init__(self):
        super().__init__(Paper)
        
    # Create
    def create_paper(self, paper: Paper, db: Session) -> Paper:
        existing_paper = self.get_by_arxiv_id(paper.arxiv_id, db)
        if existing_paper:
            return existing_paper
            
        return self.create(paper, db)

    # Get
    def get_by_arxiv_id(self, arxiv_id: str, db: Session) -> Optional[Paper]:
        return db.query(Paper).filter(Paper.arxiv_id == arxiv_id).first()