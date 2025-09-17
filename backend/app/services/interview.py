from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from app.models.interview import Interview, ApplicationStatus, WorkMode
from app.models.user import User
from app.repositories.interview import InterviewRepository
from app.schemas.interview import InterviewCreate, InterviewUpdate

class InterviewService:
    def __init__(self, db: Session):
        self.db = db
        self.interview_repo = InterviewRepository(db)

    def create_interview(self, user: User, interview_data: InterviewCreate) -> Interview:
        interview_dict = interview_data.model_dump(exclude_unset=True)
        return self.interview_repo.create_interview(
            user_id=user.id,
            **interview_dict
        )

    def get_user_interviews(
        self,
        user: User,
        status: Optional[str] = None,
        company: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interview]:
        status_enum = None
        if status:
            try:
                status_enum = ApplicationStatus(status)
            except ValueError:
                pass  # Invalid status, will be ignored
        
        return self.interview_repo.get_by_user_and_filters(
            user_id=user.id,
            status=status_enum,
            company=company,
            from_date=from_date,
            to_date=to_date,
            skip=skip,
            limit=limit
        )

    def get_interview_by_id(self, user: User, interview_id: UUID) -> Optional[Interview]:
        interview = self.interview_repo.get_by_id(interview_id)
        if interview and interview.user_id == user.id:
            return interview
        return None

    def update_interview(
        self, user: User, interview_id: UUID, interview_data: InterviewUpdate
    ) -> Optional[Interview]:
        interview = self.get_interview_by_id(user, interview_id)
        if not interview:
            return None
        
        update_dict = interview_data.model_dump(exclude_unset=True)
        return self.interview_repo.update(interview_id, update_dict)

    def delete_interview(self, user: User, interview_id: UUID) -> bool:
        interview = self.get_interview_by_id(user, interview_id)
        if not interview:
            return False
        
        return self.interview_repo.delete(interview_id)

    def count_user_interviews(self, user: User) -> int:
        return self.interview_repo.count_by_user_id(user.id)

    def get_user_interview_statistics(self, user: User) -> Dict[str, Any]:
        total_count = self.count_user_interviews(user)
        status_counts = self.interview_repo.get_status_counts(user.id)
        
        # Calculate conversion rates
        applied_count = status_counts.get("APPLIED", 0)
        offer_count = status_counts.get("OFFER", 0)
        
        conversion_rate = 0.0
        if applied_count > 0:
            conversion_rate = (offer_count / applied_count) * 100
        
        return {
            "total_interviews": total_count,
            "status_counts": status_counts,
            "conversion_rate": round(conversion_rate, 2),
            "success_rate": round((offer_count / max(total_count, 1)) * 100, 2)
        }

    def get_upcoming_interviews(self, user: User, days_ahead: int = 7) -> List[Interview]:
        return self.interview_repo.get_upcoming_interviews(user.id, days_ahead)

    def get_recent_activity(self, user: User, limit: int = 10) -> List[Interview]:
        return self.interview_repo.get_recent_activity(user.id, limit)
