from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, data: Dict[str, Any]) -> T:
        try:
            instance = self.model(**data)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e.orig)}"
            )

    def get_by_id(self, id: Any) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        instance = self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: Any) -> bool:
        instance = self.get_by_id(id)
        if not instance:
            return False
        
        self.db.delete(instance)
        self.db.commit()
        return True

    def count(self) -> int:
        return self.db.query(self.model).count()
