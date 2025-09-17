from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard import DashboardService

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary with statistics and recent activity"""
    dashboard_service = DashboardService(db)
    
    summary = dashboard_service.get_dashboard_summary(current_user)
    
    return summary

@router.get("/stats")
async def get_detailed_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed statistics for the user's interviews"""
    from app.services.interview import InterviewService
    
    interview_service = InterviewService(db)
    stats = interview_service.get_user_interview_statistics(current_user)
    
    return {
        "user_id": str(current_user.id),
        "total_interviews": stats["total_interviews"],
        "conversion_rate": stats["conversion_rate"],
        "success_rate": stats["success_rate"],
        "status_breakdown": stats["status_counts"],
        "account_created": current_user.created_at.isoformat(),
        "last_activity": current_user.updated_at.isoformat()
    }

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent interview activity"""
    from app.services.interview import InterviewService
    
    interview_service = InterviewService(db)
    recent = interview_service.get_recent_activity(current_user, limit)
    
    activity = []
    for interview in recent:
        activity.append({
            "id": str(interview.id),
            "company_name": interview.company_name,
            "role_title": interview.role_title,
            "status": interview.application_status.value,
            "updated_at": interview.updated_at.isoformat(),
            "created_at": interview.created_at.isoformat()
        })
    
    return {"recent_activity": activity}

@router.get("/upcoming")
async def get_upcoming_interviews(
    days_ahead: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming interviews"""
    from app.services.interview import InterviewService
    
    interview_service = InterviewService(db)
    upcoming = interview_service.get_upcoming_interviews(current_user, days_ahead)
    
    interviews = []
    for interview in upcoming:
        interviews.append({
            "id": str(interview.id),
            "company_name": interview.company_name,
            "role_title": interview.role_title,
            "interview_date": interview.interview_date.isoformat() if interview.interview_date else None,
            "status": interview.application_status.value,
            "location": interview.location,
            "work_mode": interview.work_mode.value
        })
    
    return {"upcoming_interviews": interviews}
