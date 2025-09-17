from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.user import User
from app.services.interview import InterviewService

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.interview_service = InterviewService(db)

    def get_dashboard_summary(self, user: User) -> Dict[str, Any]:
        # Get basic interview statistics
        stats = self.interview_service.get_user_interview_statistics(user)
        
        # Get upcoming interviews (next 7 days)
        upcoming = self.interview_service.get_upcoming_interviews(user, 7)
        
        # Get recent activity (last 10 updates)
        recent_activity = self.interview_service.get_recent_activity(user, 10)
        
        # Calculate weekly activity
        week_ago = datetime.now() - timedelta(days=7)
        recent_interviews = self.interview_service.get_user_interviews(
            user, from_date=week_ago.date(), limit=100
        )
        
        # Group status counts for chart data
        status_chart_data = []
        for status, count in stats["status_counts"].items():
            if count > 0:  # Only include statuses with data
                status_chart_data.append({
                    "status": status.replace("_", " ").title(),
                    "count": count
                })
        
        # Create timeline data for upcoming interviews
        upcoming_timeline = []
        for interview in upcoming[:5]:  # Limit to 5 most recent
            upcoming_timeline.append({
                "id": str(interview.id),
                "company_name": interview.company_name,
                "role_title": interview.role_title,
                "interview_date": interview.interview_date.isoformat() if interview.interview_date else None,
                "status": interview.application_status.value
            })
        
        # Recent activity timeline
        activity_timeline = []
        for interview in recent_activity[:5]:
            activity_timeline.append({
                "id": str(interview.id),
                "company_name": interview.company_name,
                "role_title": interview.role_title,
                "status": interview.application_status.value,
                "updated_at": interview.updated_at.isoformat()
            })
        
        return {
            "summary": {
                "total_interviews": stats["total_interviews"],
                "conversion_rate": stats["conversion_rate"],
                "success_rate": stats["success_rate"],
                "this_week_applications": len(recent_interviews)
            },
            "status_distribution": status_chart_data,
            "upcoming_interviews": upcoming_timeline,
            "recent_activity": activity_timeline,
            "insights": self._generate_insights(stats, upcoming, recent_activity)
        }

    def _generate_insights(self, stats: Dict, upcoming: List, recent: List) -> List[str]:
        insights = []
        
        # Conversion rate insights
        if stats["conversion_rate"] > 20:
            insights.append("🎉 Great conversion rate! You're doing excellent.")
        elif stats["conversion_rate"] > 10:
            insights.append("👍 Good conversion rate. Keep up the momentum!")
        elif stats["total_interviews"] > 5:
            insights.append("💪 Keep applying! Your perfect role is out there.")
        
        # Upcoming interviews
        if len(upcoming) > 0:
            insights.append(f"📅 You have {len(upcoming)} upcoming interviews this week!")
        
        # Activity insights
        if len(recent) > 3:
            insights.append("🔥 High activity! You're actively managing your job search.")
        
        # Status-specific insights
        applied_count = stats["status_counts"].get("APPLIED", 0)
        if applied_count > 10:
            insights.append("📊 Great job staying active with applications!")
        
        if not insights:
            insights.append("🚀 Ready to track your next interview? Click 'New Interview' to get started!")
        
        return insights
