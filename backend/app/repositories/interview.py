from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date
from uuid import UUID

from app.models.interview import Interview, ApplicationStatus, WorkMode
from app.repositories.base import BaseRepository

class InterviewRepository(BaseRepository[Interview]):
    def __init__(self, db: Session):
        super().__init__(db, Interview)

    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Interview]:
        return (
            self.db.query(Interview)
            .filter(Interview.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Interview.created_at.desc())
            .all()
        )

    def get_by_user_and_filters(
        self,
        user_id: UUID,
        status: Optional[ApplicationStatus] = None,
        company: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interview]:
        query = self.db.query(Interview).filter(Interview.user_id == user_id)
        
        if status:
            query = query.filter(Interview.application_status == status)
        
        if company:
            query = query.filter(Interview.company_name.ilike(f"%{company}%"))
        
        if from_date:
            query = query.filter(Interview.created_at >= from_date)
        
        if to_date:
            query = query.filter(Interview.created_at <= to_date)
        
        return (
            query
            .offset(skip)
            .limit(limit)
            .order_by(Interview.created_at.desc())
            .all()
        )

    def count_by_user_id(self, user_id: UUID) -> int:
        return self.db.query(Interview).filter(Interview.user_id == user_id).count()

    def count_by_status_and_user(self, user_id: UUID, status: ApplicationStatus) -> int:
        return (
            self.db.query(Interview)
            .filter(and_(Interview.user_id == user_id, Interview.application_status == status))
            .count()
        )

    def get_status_counts(self, user_id: UUID) -> Dict[str, int]:
        counts = {}
        for status in ApplicationStatus:
            counts[status.value] = self.count_by_status_and_user(user_id, status)
        return counts

    def get_upcoming_interviews(self, user_id: UUID, days_ahead: int = 7) -> List[Interview]:
        from_date = datetime.now()
        to_date = datetime.now().replace(hour=23, minute=59, second=59)
        # Add days_ahead to the to_date
        from datetime import timedelta
        to_date = to_date + timedelta(days=days_ahead)
        
        return (
            self.db.query(Interview)
            .filter(
                and_(
                    Interview.user_id == user_id,
                    Interview.interview_date >= from_date,
                    Interview.interview_date <= to_date
                )
            )
            .order_by(Interview.interview_date)
            .all()
        )

    def get_recent_activity(self, user_id: UUID, limit: int = 10) -> List[Interview]:
        return (
            self.db.query(Interview)
            .filter(Interview.user_id == user_id)
            .order_by(Interview.updated_at.desc())
            .limit(limit)
            .all()
        )

    def create_interview(
        self,
        user_id: UUID,
        company_name: str,
        role_title: str,
        work_mode: WorkMode,
        **kwargs
    ) -> Interview:
        interview_data = {
            "user_id": user_id,
            "company_name": company_name,
            "role_title": role_title,
            "work_mode": work_mode,
            **kwargs
        }
        return self.create(interview_data)
