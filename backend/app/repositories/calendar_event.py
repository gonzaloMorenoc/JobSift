from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.calendar_event import CalendarEvent
from app.repositories.base import BaseRepository

class CalendarEventRepository(BaseRepository[CalendarEvent]):
    def __init__(self, db: Session):
        super().__init__(db, CalendarEvent)

    def get_by_interview_id(self, interview_id: UUID) -> List[CalendarEvent]:
        return (
            self.db.query(CalendarEvent)
            .filter(CalendarEvent.interview_id == interview_id)
            .order_by(CalendarEvent.start_time)
            .all()
        )

    def get_by_external_id(self, external_event_id: str, provider: str) -> Optional[CalendarEvent]:
        return (
            self.db.query(CalendarEvent)
            .filter(
                CalendarEvent.external_event_id == external_event_id,
                CalendarEvent.calendar_provider == provider
            )
            .first()
        )

    def get_upcoming_events(self, user_id: UUID, days_ahead: int = 30) -> List[CalendarEvent]:
        from app.models.interview import Interview
        from datetime import timedelta
        
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        return (
            self.db.query(CalendarEvent)
            .join(Interview)
            .filter(
                Interview.user_id == user_id,
                CalendarEvent.start_time >= datetime.now(),
                CalendarEvent.start_time <= end_date
            )
            .order_by(CalendarEvent.start_time)
            .all()
        )

    def create_calendar_event(
        self,
        interview_id: UUID,
        calendar_provider: str,
        event_title: str,
        start_time: datetime,
        end_time: datetime,
        **kwargs
    ) -> CalendarEvent:
        event_data = {
            "interview_id": interview_id,
            "calendar_provider": calendar_provider,
            "event_title": event_title,
            "start_time": start_time,
            "end_time": end_time,
            **kwargs
        }
        return self.create(event_data)

    def mark_as_synced(self, event_id: UUID, external_event_id: str) -> Optional[CalendarEvent]:
        event = self.get_by_id(event_id)
        if event:
            event.external_event_id = external_event_id
            event.is_synced = True
            self.db.commit()
            self.db.refresh(event)
        return event
