from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password_hash: str, full_name: str, locale: str = "en") -> User:
        user_data = {
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name,
            "locale": locale
        }
        return self.create(user_data)