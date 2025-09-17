from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.models.interview import ApplicationStatus, WorkMode

class InterviewBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=100)
    company_description: Optional[str] = Field(None, max_length=1000)
    role_title: str = Field(..., min_length=1, max_length=100)
    work_mode: WorkMode
    location: Optional[str] = Field(None, max_length=100)
    application_status: Optional[ApplicationStatus] = ApplicationStatus.APPLIED
    next_milestone: Optional[str] = Field(None, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=20)
    salary_range_min: Optional[Decimal] = Field(None, ge=0)
    salary_range_max: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field("USD", min_length=3, max_length=3)
    language: Optional[str] = Field("en", min_length=2, max_length=5)
    travel_requirements: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=2000)
    interview_date: Optional[datetime] = None

    @validator('salary_range_max')
    def salary_max_must_be_greater_than_min(cls, v, values):
        if v is not None and 'salary_range_min' in values and values['salary_range_min'] is not None:
            if v < values['salary_range_min']:
                raise ValueError('salary_range_max must be greater than or equal to salary_range_min')
        return v

    @validator('currency')
    def currency_must_be_uppercase(cls, v):
        return v.upper() if v else v

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=100)
    company_description: Optional[str] = Field(None, max_length=1000)
    role_title: Optional[str] = Field(None, min_length=1, max_length=100)
    work_mode: Optional[WorkMode] = None
    location: Optional[str] = Field(None, max_length=100)
    application_status: Optional[ApplicationStatus] = None
    next_milestone: Optional[str] = Field(None, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=20)
    salary_range_min: Optional[Decimal] = Field(None, ge=0)
    salary_range_max: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    language: Optional[str] = Field(None, min_length=2, max_length=5)
    travel_requirements: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=2000)
    interview_date: Optional[datetime] = None

    @validator('currency')
    def currency_must_be_uppercase(cls, v):
        return v.upper() if v else v

class InterviewInDB(InterviewBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Interview(InterviewInDB):
    pass

class InterviewsResponse(BaseModel):
    interviews: List[Interview]
    total: int
    skip: int
    limit: int

# Status and mode enums for frontend
class InterviewStatusInfo(BaseModel):
    value: str
    label: str
    color: str

class WorkModeInfo(BaseModel):
    value: str
    label: str
    icon: str

class InterviewMetadata(BaseModel):
    statuses: List[InterviewStatusInfo]
    work_modes: List[WorkModeInfo]
    currencies: List[str]

# Default metadata
DEFAULT_INTERVIEW_METADATA = InterviewMetadata(
    statuses=[
        InterviewStatusInfo(value="APPLIED", label="Applied", color="blue"),
        InterviewStatusInfo(value="SCREENING", label="Screening", color="yellow"),
        InterviewStatusInfo(value="HR_INTERVIEW", label="HR Interview", color="orange"),
        InterviewStatusInfo(value="TECH_INTERVIEW", label="Technical Interview", color="purple"),
        InterviewStatusInfo(value="MANAGER_INTERVIEW", label="Manager Interview", color="indigo"),
        InterviewStatusInfo(value="OFFER", label="Offer", color="green"),
        InterviewStatusInfo(value="REJECTED", label="Rejected", color="red"),
        InterviewStatusInfo(value="ON_HOLD", label="On Hold", color="gray"),
    ],
    work_modes=[
        WorkModeInfo(value="REMOTE", label="Remote", icon="🏠"),
        WorkModeInfo(value="HYBRID", label="Hybrid", icon="🏢"),
        WorkModeInfo(value="ONSITE", label="On-site", icon="🏬"),
    ],
    currencies=["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF", "SEK", "NOK", "DKK"]
)
