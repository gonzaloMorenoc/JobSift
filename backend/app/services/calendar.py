from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from io import StringIO

from app.models.user import User
from app.models.interview import Interview
from app.models.calendar_event import CalendarEvent
from app.repositories.calendar_event import CalendarEventRepository
from app.repositories.interview import InterviewRepository

class CalendarService:
    def __init__(self, db: Session):
        self.db = db
        self.calendar_repo = CalendarEventRepository(db)
        self.interview_repo = InterviewRepository(db)

    def create_calendar_event(
        self,
        user: User,
        interview_id: UUID,
        event_details: Dict[str, Any]
    ) -> CalendarEvent:
        # Verify user owns the interview
        interview = self.interview_repo.get_by_id(interview_id)
        if not interview or interview.user_id != user.id:
            raise ValueError("Interview not found or access denied")

        return self.calendar_repo.create_calendar_event(
            interview_id=interview_id,
            **event_details
        )

    def sync_with_google_calendar(self, user: User, interview_id: UUID) -> Dict[str, str]:
        """
        Sync interview with Google Calendar (Mock implementation)
        In production, this would use Google Calendar API
        """
        interview = self.interview_repo.get_by_id(interview_id)
        if not interview or interview.user_id != user.id:
            raise ValueError("Interview not found or access denied")

        if not interview.interview_date:
            raise ValueError("Interview date is required for calendar sync")

        # Mock Google Calendar sync
        mock_event_id = f"google_event_{interview_id}"
        mock_calendar_url = f"https://calendar.google.com/calendar/event?eid={mock_event_id}"

        # Create calendar event record
        event_title = f"Interview: {interview.role_title} at {interview.company_name}"
        event_description = f"""
Interview Details:
- Company: {interview.company_name}
- Role: {interview.role_title}
- Location: {interview.location or 'Not specified'}
- Contact: {interview.contact_name or 'Not specified'}
- Notes: {interview.notes or 'No additional notes'}
        """.strip()

        calendar_event = self.calendar_repo.create_calendar_event(
            interview_id=interview_id,
            calendar_provider="google",
            event_title=event_title,
            event_description=event_description,
            start_time=interview.interview_date,
            end_time=interview.interview_date + timedelta(hours=1),
            external_event_id=mock_event_id,
            is_synced=True
        )

        return {
            "event_id": mock_event_id,
            "calendar_url": mock_calendar_url,
            "message": "Interview synced with Google Calendar (Mock)"
        }

    def generate_ics_feed(self, user: User, days_ahead: int = 90) -> str:
        """Generate ICS calendar feed for user's interviews"""
        interviews = self.interview_repo.get_upcoming_interviews(user.id, days_ahead)
        
        # ICS header
        ics_content = StringIO()
        ics_content.write("BEGIN:VCALENDAR\r\n")
        ics_content.write("VERSION:2.0\r\n")
        ics_content.write("PRODID:-//JobSift//JobSift Calendar//EN\r\n")
        ics_content.write("CALSCALE:GREGORIAN\r\n")
        ics_content.write("METHOD:PUBLISH\r\n")
        ics_content.write("X-WR-CALNAME:JobSift Interviews\r\n")
        ics_content.write("X-WR-CALDESC:Your job interview schedule from JobSift\r\n")

        for interview in interviews:
            if interview.interview_date:
                self._add_interview_to_ics(ics_content, interview)

        ics_content.write("END:VCALENDAR\r\n")
        return ics_content.getvalue()

    def _add_interview_to_ics(self, ics_content: StringIO, interview: Interview):
        """Add a single interview to ICS content"""
        # Generate unique event ID
        event_uid = f"interview-{interview.id}@jobsift.com"
        
        # Format dates for ICS (UTC)
        start_time = interview.interview_date.strftime("%Y%m%dT%H%M%SZ")
        end_time = (interview.interview_date + timedelta(hours=1)).strftime("%Y%m%dT%H%M%SZ")
        created_time = interview.created_at.strftime("%Y%m%dT%H%M%SZ")
        
        # Event summary and description
        summary = f"Interview: {interview.role_title} at {interview.company_name}"
        description = f"""Job Interview Details:
Company: {interview.company_name}
Role: {interview.role_title}
Status: {interview.application_status.value}
Location: {interview.location or 'TBD'}
Contact: {interview.contact_name or 'TBD'}

Notes: {interview.notes or 'No additional notes'}"""

        ics_content.write("BEGIN:VEVENT\r\n")
        ics_content.write(f"UID:{event_uid}\r\n")
        ics_content.write(f"DTSTART:{start_time}\r\n")
        ics_content.write(f"DTEND:{end_time}\r\n")
        ics_content.write(f"DTSTAMP:{created_time}\r\n")
        ics_content.write(f"SUMMARY:{summary}\r\n")
        ics_content.write(f"DESCRIPTION:{self._escape_ics_text(description)}\r\n")
        
        if interview.location:
            ics_content.write(f"LOCATION:{self._escape_ics_text(interview.location)}\r\n")
        
        ics_content.write("STATUS:CONFIRMED\r\n")
        ics_content.write("TRANSP:OPAQUE\r\n")
        ics_content.write("CATEGORIES:INTERVIEW,JOBSEARCH\r\n")
        ics_content.write("END:VEVENT\r\n")

    def _escape_ics_text(self, text: str) -> str:
        """Escape special characters in ICS text fields"""
        if not text:
            return ""
        
        # Replace newlines and escape special characters
        text = text.replace("\\", "\\\\")
        text = text.replace(",", "\\,")
        text = text.replace(";", "\\;")
        text = text.replace("\n", "\\n")
        text = text.replace("\r", "")
        
        return text

    def get_user_calendar_events(
        self, 
        user: User, 
        days_ahead: int = 30
    ) -> List[CalendarEvent]:
        """Get upcoming calendar events for user"""
        return self.calendar_repo.get_upcoming_events(user.id, days_ahead)

    def delete_calendar_event(self, user: User, event_id: UUID) -> bool:
        """Delete a calendar event (and unsync from external calendar)"""
        event = self.calendar_repo.get_by_id(event_id)
        if not event:
            return False
        
        # Verify user owns the interview associated with this event
        interview = self.interview_repo.get_by_id(event.interview_id)
        if not interview or interview.user_id != user.id:
            return False
        
        # In production, this would also delete from external calendar
        # For now, just delete from our database
        return self.calendar_repo.delete(event_id)

    def get_calendar_integration_status(self, user: User) -> Dict[str, Any]:
        """Get status of calendar integrations for user"""
        # Count synced events
        events = self.calendar_repo.get_upcoming_events(user.id, 365)  # Next year
        
        synced_count = len([e for e in events if e.is_synced])
        total_count = len(events)
        
        return {
            "total_events": total_count,
            "synced_events": synced_count,
            "google_calendar_connected": False,  # Mock - would check OAuth status
            "apple_calendar_available": True,    # ICS feed is always available
            "sync_percentage": (synced_count / max(total_count, 1)) * 100
        }
