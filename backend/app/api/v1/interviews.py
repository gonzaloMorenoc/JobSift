from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.interview import (
    Interview,
    InterviewCreate,
    InterviewUpdate,
    InterviewsResponse,
    DEFAULT_INTERVIEW_METADATA,
    InterviewMetadata
)
from app.services.interview import InterviewService

router = APIRouter()

@router.get("/metadata", response_model=InterviewMetadata)
async def get_interview_metadata():
    """Get interview metadata (statuses, work modes, currencies)"""
    return DEFAULT_INTERVIEW_METADATA

@router.get("", response_model=InterviewsResponse)
async def get_interviews(
    status: Optional[str] = Query(None, description="Filter by application status"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    from_date: Optional[date] = Query(None, description="Filter interviews created from this date"),
    to_date: Optional[date] = Query(None, description="Filter interviews created until this date"),
    skip: int = Query(0, ge=0, description="Number of interviews to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of interviews to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's interviews with optional filtering"""
    interview_service = InterviewService(db)
    
    interviews = interview_service.get_user_interviews(
        user=current_user,
        status=status,
        company=company,
        from_date=from_date,
        to_date=to_date,
        skip=skip,
        limit=limit
    )
    
    total = interview_service.count_user_interviews(current_user)
    
    return InterviewsResponse(
        interviews=interviews,
        total=total,
        skip=skip,
        limit=limit
    )

@router.post("", response_model=Interview, status_code=status.HTTP_201_CREATED)
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new interview"""
    interview_service = InterviewService(db)
    
    interview = interview_service.create_interview(
        user=current_user,
        interview_data=interview_data
    )
    
    return interview

@router.get("/{interview_id}", response_model=Interview)
async def get_interview(
    interview_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific interview by ID"""
    interview_service = InterviewService(db)
    
    interview = interview_service.get_interview_by_id(
        user=current_user,
        interview_id=interview_id
    )
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return interview

@router.put("/{interview_id}", response_model=Interview)
async def update_interview(
    interview_id: UUID,
    interview_data: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing interview"""
    interview_service = InterviewService(db)
    
    interview = interview_service.update_interview(
        user=current_user,
        interview_id=interview_id,
        interview_data=interview_data
    )
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return interview

@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interview(
    interview_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an interview"""
    interview_service = InterviewService(db)
    
    success = interview_service.delete_interview(
        user=current_user,
        interview_id=interview_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

@router.get("/{interview_id}/stats")
async def get_interview_stats(
    interview_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific interview (future enhancement)"""
    interview_service = InterviewService(db)
    
    interview = interview_service.get_interview_by_id(
        user=current_user,
        interview_id=interview_id
    )
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Basic stats - can be enhanced later
    return {
        "id": str(interview.id),
        "days_since_application": (interview.updated_at.date() - interview.created_at.date()).days,
        "current_status": interview.application_status.value,
        "has_salary_info": interview.salary_range_min is not None,
        "has_contact_info": interview.contact_email is not None or interview.contact_phone is not None,
        "has_interview_date": interview.interview_date is not None
    }
