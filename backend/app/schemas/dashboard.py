from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class StatusDistributionItem(BaseModel):
    status: str
    count: int

class UpcomingInterview(BaseModel):
    id: str
    company_name: str
    role_title: str
    interview_date: Optional[str] = None
    status: str

class RecentActivity(BaseModel):
    id: str
    company_name: str
    role_title: str
    status: str
    updated_at: str

class DashboardSummaryStats(BaseModel):
    total_interviews: int
    conversion_rate: float
    success_rate: float
    this_week_applications: int

class DashboardSummary(BaseModel):
    summary: DashboardSummaryStats
    status_distribution: List[StatusDistributionItem]
    upcoming_interviews: List[UpcomingInterview]
    recent_activity: List[RecentActivity]
    insights: List[str]

# Additional analytics models for future use
class MonthlyStats(BaseModel):
    month: str
    applications: int
    interviews: int
    offers: int

class CompanyStats(BaseModel):
    company_name: str
    total_applications: int
    current_status: str
    last_activity: datetime

class Analytics(BaseModel):
    monthly_trends: List[MonthlyStats]
    top_companies: List[CompanyStats]
    average_time_to_response: Optional[float] = None
    best_performing_day: Optional[str] = None
    
class DashboardAnalytics(BaseModel):
    summary: DashboardSummary
    analytics: Optional[Analytics] = None
