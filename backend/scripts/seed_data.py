#!/usr/bin/env python3
"""
JobSift Database Seeding Script
Creates demo user and sample interviews for development and testing
"""

import asyncio
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.interview import Interview, ApplicationStatus, WorkMode
from app.models.calendar_event import CalendarEvent

def create_demo_user(db):
    """Create a demo user for testing"""
    # Check if demo user already exists
    existing_user = db.query(User).filter(User.email == "demo@jobsift.com").first()
    if existing_user:
        print("📧 Demo user already exists: demo@jobsift.com")
        return existing_user
    
    demo_user = User(
        email="demo@jobsift.com",
        password_hash=get_password_hash("demo123456"),
        full_name="Demo User",
        locale="en",
        is_verified=True,
        is_active=True
    )
    
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    
    print("✅ Created demo user: demo@jobsift.com / demo123456")
    return demo_user

def create_sample_interviews(db, user_id):
    """Create sample interviews for demo purposes"""
    # Check if interviews already exist
    existing_count = db.query(Interview).filter(Interview.user_id == user_id).count()
    if existing_count > 0:
        print(f"📊 User already has {existing_count} interviews")
        return
    
    sample_interviews = [
        {
            "company_name": "TechCorp Inc",
            "company_description": "Leading technology company specializing in cloud solutions",
            "role_title": "Senior Full Stack Developer",
            "work_mode": WorkMode.REMOTE,
            "location": "San Francisco, CA",
            "application_status": ApplicationStatus.TECH_INTERVIEW,
            "next_milestone": "Final interview with CTO",
            "contact_name": "Sarah Johnson",
            "contact_email": "sarah.johnson@techcorp.com",
            "contact_phone": "+1-555-123-4567",
            "salary_range_min": Decimal("120000"),
            "salary_range_max": Decimal("150000"),
            "currency": "USD",
            "language": "en",
            "notes": "Great company culture. Technical interview went well.",
            "interview_date": datetime.now() + timedelta(days=3)
        },
        {
            "company_name": "StartupXYZ",
            "company_description": "Fast-growing fintech startup",
            "role_title": "Frontend Developer",
            "work_mode": WorkMode.HYBRID,
            "location": "New York, NY",
            "application_status": ApplicationStatus.HR_INTERVIEW,
            "next_milestone": "Technical coding challenge",
            "contact_name": "Mike Chen",
            "contact_email": "mike.chen@startupxyz.com",
            "salary_range_min": Decimal("90000"),
            "salary_range_max": Decimal("110000"),
            "currency": "USD",
            "notes": "Exciting product, young team",
            "interview_date": datetime.now() + timedelta(days=5)
        },
        {
            "company_name": "GlobalSoft",
            "company_description": "Enterprise software solutions provider",
            "role_title": "Software Engineer II",
            "work_mode": WorkMode.ONSITE,
            "location": "Austin, TX",
            "application_status": ApplicationStatus.APPLIED,
            "contact_email": "hr@globalsoft.com",
            "salary_range_min": Decimal("95000"),
            "salary_range_max": Decimal("125000"),
            "currency": "USD",
            "notes": "Applied through LinkedIn, waiting for response"
        },
        {
            "company_name": "InnovateNow",
            "role_title": "React Developer",
            "work_mode": WorkMode.REMOTE,
            "application_status": ApplicationStatus.OFFER,
            "next_milestone": "Salary negotiation",
            "contact_name": "Lisa Rodriguez",
            "contact_email": "lisa@innovatenow.com",
            "salary_range_min": Decimal("105000"),
            "salary_range_max": Decimal("120000"),
            "currency": "USD",
            "notes": "Received offer! Need to negotiate remote work allowance."
        },
        {
            "company_name": "DataDriven Co",
            "role_title": "Full Stack Developer",
            "work_mode": WorkMode.HYBRID,
            "location": "Seattle, WA",
            "application_status": ApplicationStatus.REJECTED,
            "notes": "Not a good fit for the team dynamics",
            "salary_range_min": Decimal("100000"),
            "salary_range_max": Decimal("130000"),
            "currency": "USD"
        },
        {
            "company_name": "CloudFirst",
            "company_description": "Cloud infrastructure and DevOps solutions",
            "role_title": "DevOps Engineer",
            "work_mode": WorkMode.REMOTE,
            "application_status": ApplicationStatus.SCREENING,
            "next_milestone": "Phone screening with hiring manager",
            "contact_name": "Alex Thompson",
            "contact_email": "alex@cloudfirst.com",
            "salary_range_min": Decimal("110000"),
            "salary_range_max": Decimal("140000"),
            "currency": "USD",
            "notes": "Strong focus on AWS and Kubernetes",
            "interview_date": datetime.now() + timedelta(days=2)
        },
        {
            "company_name": "MobileFirst",
            "role_title": "React Native Developer",
            "work_mode": WorkMode.ONSITE,
            "location": "Los Angeles, CA",
            "application_status": ApplicationStatus.ON_HOLD,
            "notes": "Hiring freeze due to budget constraints",
            "salary_range_min": Decimal("95000"),
            "salary_range_max": Decimal("115000"),
            "currency": "USD"
        },
        {
            "company_name": "EcoTech Solutions",
            "company_description": "Sustainable technology for environmental impact",
            "role_title": "Senior JavaScript Developer",
            "work_mode": WorkMode.REMOTE,
            "application_status": ApplicationStatus.MANAGER_INTERVIEW,
            "next_milestone": "Meet with VP of Engineering",
            "contact_name": "Emma Green",
            "contact_email": "emma@ecotech.com",
            "salary_range_min": Decimal("115000"),
            "salary_range_max": Decimal("135000"),
            "currency": "USD",
            "notes": "Mission-driven company, great values alignment",
            "interview_date": datetime.now() + timedelta(days=7)
        }
    ]
    
    created_interviews = []
    
    for interview_data in sample_interviews:
        # Add some random variance to created_at dates
        created_days_ago = len(created_interviews) + 1
        created_at = datetime.now() - timedelta(days=created_days_ago)
        
        interview = Interview(
            user_id=user_id,
            created_at=created_at,
            updated_at=created_at,
            **interview_data
        )
        
        db.add(interview)
        created_interviews.append(interview)
    
    db.commit()
    print(f"✅ Created {len(created_interviews)} sample interviews")
    
    return created_interviews

def create_demo_calendar_events(db, interviews):
    """Create some demo calendar events"""
    for interview in interviews:
        if interview.interview_date and interview.application_status in [
            ApplicationStatus.TECH_INTERVIEW,
            ApplicationStatus.HR_INTERVIEW,
            ApplicationStatus.MANAGER_INTERVIEW
        ]:
            event = CalendarEvent(
                interview_id=interview.id,
                external_event_id=f"demo_event_{interview.id}",
                calendar_provider="google",
                event_title=f"Interview: {interview.role_title} at {interview.company_name}",
                event_description=f"Interview for {interview.role_title} position",
                start_time=interview.interview_date,
                end_time=interview.interview_date + timedelta(hours=1),
                is_synced=False
            )
            db.add(event)
    
    db.commit()
    print("✅ Created demo calendar events")

def main():
    """Main seeding function"""
    print("🌱 Starting JobSift database seeding...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create demo user
        demo_user = create_demo_user(db)
        
        # Create sample interviews
        interviews = create_sample_interviews(db, demo_user.id)
        
        # Create calendar events if interviews were created
        if interviews:
            create_demo_calendar_events(db, interviews)
        
        print("\n🎉 Database seeding completed successfully!")
        print("\n📝 Demo Credentials:")
        print("   Email: demo@jobsift.com")
        print("   Password: demo123456")
        print("\n🚀 You can now start the application with: make dev")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
