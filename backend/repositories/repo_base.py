from typing import Type, TypeVar, Generic, Optional, List, Dict, Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

T = TypeVar("T")
class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    # Create
    def create(self, obj_in: T, db: Session) -> T:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    # Read
    def getById(self, id: int, db: Session) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def getAll(self, limit: int, offset: int, db: Session) -> List[T]:
        return db.query(self.model).limit(limit).offset(offset).all()
    
    # Update
    def update(self, obj: T, update_data: Dict[str, Any], db: Session) -> Optional[T]:
        for key, value in update_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    # Delete
    def delete(self, obj: T, db: Session) -> Optional[T]:
        db.delete(obj)
        db.commit()
        return obj