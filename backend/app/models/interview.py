from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base

class WorkMode(enum.Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"

class ApplicationStatus(enum.Enum):
    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    HR_INTERVIEW = "HR_INTERVIEW"
    TECH_INTERVIEW = "TECH_INTERVIEW"
    MANAGER_INTERVIEW = "MANAGER_INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    ON_HOLD = "ON_HOLD"

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Company info
    company_name = Column(String(100), nullable=False)
    company_description = Column(Text)
    
    # Role info
    role_title = Column(String(100), nullable=False)
    work_mode = Column(Enum(WorkMode), nullable=False)
    location = Column(String(100))
    
    # Process info
    application_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    next_milestone = Column(String(200))
    
    # Contact info
    contact_name = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    
    # Compensation
    salary_range_min = Column(Numeric(10, 2))
    salary_range_max = Column(Numeric(10, 2))
    currency = Column(String(3), default="USD")
    
    # Additional info
    language = Column(String(5), default="en")
    travel_requirements = Column(Text)
    notes = Column(Text)
    
    # Dates
    interview_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="interviews")
    calendar_events = relationship("CalendarEvent", back_populates="interview", cascade="all, delete-orphan")