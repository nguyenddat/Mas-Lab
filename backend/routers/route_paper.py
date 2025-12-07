import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models.model_paper import Paper
from utils import download_pdf
from services import PaperService
from schemas.schema_paper import PaperCreateRequest

router = APIRouter(prefix="/papers")

@router.post("/")
def create_paper(request: PaperCreateRequest, db: Session = Depends(get_db)):
    download_url = request.download_url

    # Tải pdf_url về Artifact Dir
    pdf_url, pdf_path = download_pdf(download_url)
    
    # Tạo paper trong database
    paper = Paper(**request.dict(), pdf_url=pdf_url)
    try:
        paper = PaperService.create_paper(paper, db)
        return paper
    except Exception as e:
        os.remove(pdf_path)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/static/{pdf_url}")
def get_static_pdf(pdf_url: str):
    return FileResponse(pdf_url)