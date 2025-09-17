from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CalendarEventBase(BaseModel):
    interview_id: UUID
    calendar_provider: str = Field(..., max_length=50)
    event_title: str = Field(..., max_length=200)
    event_description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class CalendarEventCreate(CalendarEventBase):
    pass

class CalendarEventUpdate(BaseModel):
    event_title: Optional[str] = Field(None, max_length=200)
    event_description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class CalendarEventInDB(CalendarEventBase):
    id: UUID
    external_event_id: Optional[str] = None
    is_synced: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CalendarEvent(CalendarEventInDB):
    pass

class CalendarEventsResponse(BaseModel):
    events: List[CalendarEvent]
    total: int
    days_ahead: int

class GoogleCalendarSyncRequest(BaseModel):
    interview_id: UUID

class GoogleCalendarSyncResponse(BaseModel):
    event_id: str
    calendar_url: str
    message: str

class CalendarIntegrationStatus(BaseModel):
    total_events: int
    synced_events: int
    google_calendar_connected: bool
    apple_calendar_available: bool
    sync_percentage: float

class CalendarFeedInfo(BaseModel):
    name: str
    url: Optional[str] = None
    description: str
    status: Optional[str] = None
    supported_apps: Optional[List[str]] = None

class CalendarFeeds(BaseModel):
    feeds: dict
    instructions: dict

# ICS Export settings
class ICSExportSettings(BaseModel):
    days_ahead: int = Field(default=90, ge=1, le=365)
    include_notes: bool = True
    include_contact_info: bool = True
    include_salary_info: bool = False  # Privacy setting
    
class ICSExportResponse(BaseModel):
    content: str
    filename: str
    content_type: str = "text/calendar"
