from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user import UserRepository

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def create_user(self, user_in: UserCreate) -> User:
        password_hash = get_password_hash(user_in.password)
        user = self.user_repo.create_user(
            email=user_in.email,
            password_hash=password_hash,
            full_name=user_in.full_name,
            locale=user_in.locale or "en"
        )
        return user