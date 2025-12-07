from sqlalchemy import Column, Integer, String, JSON

from models.model_base import Base

class Paper(Base):
    arxiv_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)

    pdf_url = Column(String, nullable=False)
    download_url = Column(String, nullable=False)