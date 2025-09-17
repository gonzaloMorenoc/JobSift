from typing import Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.calendar import CalendarService

router = APIRouter()

@router.post("/google/sync")
async def sync_with_google_calendar(
    request: Dict[str, UUID],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Sync interview with Google Calendar"""
    calendar_service = CalendarService(db)
    
    interview_id = request.get("interview_id")
    if not interview_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="interview_id is required"
        )
    
    try:
        result = calendar_service.sync_with_google_calendar(current_user, interview_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync with Google Calendar: {str(e)}"
        )

@router.get("/ics")
async def export_ics_feed(
    response: Response,
    days_ahead: int = Query(90, ge=1, le=365, description="Number of days ahead to include"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user's interviews as ICS calendar feed"""
    calendar_service = CalendarService(db)
    
    try:
        ics_content = calendar_service.generate_ics_feed(current_user, days_ahead)
        
        response.headers["Content-Type"] = "text/calendar; charset=utf-8"
        response.headers["Content-Disposition"] = "attachment; filename=jobsift_interviews.ics"
        response.headers["Cache-Control"] = "no-cache"
        
        return Response(content=ics_content, media_type="text/calendar")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ICS feed: {str(e)}"
        )

@router.get("/events")
async def get_calendar_events(
    days_ahead: int = Query(30, ge=1, le=365, description="Number of days ahead to include"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's upcoming calendar events"""
    calendar_service = CalendarService(db)
    
    events = calendar_service.get_user_calendar_events(current_user, days_ahead)
    
    event_list = []
    for event in events:
        event_list.append({
            "id": str(event.id),
            "interview_id": str(event.interview_id),
            "title": event.event_title,
            "description": event.event_description,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat(),
            "provider": event.calendar_provider,
            "is_synced": event.is_synced,
            "external_event_id": event.external_event_id
        })
    
    return {
        "events": event_list,
        "total": len(event_list),
        "days_ahead": days_ahead
    }

@router.delete("/events/{event_id}")
async def delete_calendar_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a calendar event"""
    calendar_service = CalendarService(db)
    
    success = calendar_service.delete_calendar_event(current_user, event_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar event not found"
        )
    
    return {"message": "Calendar event deleted successfully"}

@router.get("/integration-status")
async def get_calendar_integration_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get calendar integration status for user"""
    calendar_service = CalendarService(db)
    
    status_info = calendar_service.get_calendar_integration_status(current_user)
    
    return status_info

@router.post("/microsoft/sync")
async def sync_with_microsoft_calendar(
    request: Dict[str, UUID],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync interview with Microsoft Calendar (placeholder)"""
    # Placeholder for future Microsoft Calendar integration
    return {
        "message": "Microsoft Calendar integration coming soon!",
        "status": "not_implemented"
    }

@router.get("/feeds")
async def get_calendar_feeds(
    current_user: User = Depends(get_current_user)
):
    """Get available calendar feed URLs for user"""
    base_url = "https://api.jobsift.com"  # In production, get from config
    
    return {
        "feeds": {
            "ics": {
                "name": "ICS Feed (Apple Calendar, Outlook, etc.)",
                "url": f"{base_url}/api/v1/calendar/ics",
                "description": "Subscribe to this feed in your calendar app to see your interviews",
                "supported_apps": ["Apple Calendar", "Google Calendar", "Outlook", "Thunderbird"]
            },
            "google": {
                "name": "Google Calendar Sync",
                "description": "Sync individual interviews with your Google Calendar",
                "status": "available"
            },
            "microsoft": {
                "name": "Microsoft Calendar Sync",
                "description": "Sync with Outlook/Microsoft Calendar",
                "status": "coming_soon"
            }
        },
        "instructions": {
            "apple_calendar": "Settings → Accounts → Add Account → Other → Calendar → Enter the ICS URL",
            "google_calendar": "Use the sync button on individual interviews",
            "outlook": "File → Account Settings → Internet Calendars → New → Enter the ICS URL"
        }
    }

# Health check endpoint for calendar service
@router.get("/health")
async def calendar_health_check():
    """Health check for calendar service"""
    return {
        "service": "calendar",
        "status": "healthy",
        "features": {
            "ics_export": "available",
            "google_sync": "mock_available",
            "microsoft_sync": "planned"
        }
    }
