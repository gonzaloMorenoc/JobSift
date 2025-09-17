def test_dashboard_summary_empty(client, authenticated_user):
    """Test dashboard summary with no interviews"""
    response = client.get("/api/v1/dashboard/summary", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert "summary" in data
    assert data["summary"]["total_interviews"] == 0
    assert data["summary"]["conversion_rate"] == 0.0
    assert "status_distribution" in data
    assert "upcoming_interviews" in data
    assert "recent_activity" in data
    assert "insights" in data

def test_dashboard_summary_with_data(client, authenticated_user):
    """Test dashboard summary with interview data"""
    # Create some interviews
    interviews = [
        {"company_name": "Company A", "role_title": "Engineer", "work_mode": "REMOTE", "application_status": "APPLIED"},
        {"company_name": "Company B", "role_title": "Developer", "work_mode": "HYBRID", "application_status": "SCREENING"},
        {"company_name": "Company C", "role_title": "Manager", "work_mode": "ONSITE", "application_status": "OFFER"},
    ]
    
    for interview_data in interviews:
        client.post("/api/v1/interviews", json=interview_data, headers=authenticated_user)
    
    # Get dashboard summary
    response = client.get("/api/v1/dashboard/summary", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert data["summary"]["total_interviews"] == 3
    assert data["summary"]["conversion_rate"] > 0  # Should have some conversion
    assert len(data["status_distribution"]) > 0
    assert len(data["insights"]) > 0

def test_dashboard_detailed_stats(client, authenticated_user):
    """Test detailed dashboard statistics"""
    # Create an interview first
    interview_data = {
        "company_name": "Test Company",
        "role_title": "Test Role",
        "work_mode": "REMOTE"
    }
    client.post("/api/v1/interviews", json=interview_data, headers=authenticated_user)
    
    response = client.get("/api/v1/dashboard/stats", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert "total_interviews" in data
    assert "conversion_rate" in data
    assert "success_rate" in data
    assert "status_breakdown" in data
    assert "user_id" in data

def test_dashboard_recent_activity(client, authenticated_user):
    """Test recent activity endpoint"""
    response = client.get("/api/v1/dashboard/recent-activity", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert "recent_activity" in data
    assert isinstance(data["recent_activity"], list)

def test_dashboard_upcoming_interviews(client, authenticated_user):
    """Test upcoming interviews endpoint"""
    response = client.get("/api/v1/dashboard/upcoming", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert "upcoming_interviews" in data
    assert isinstance(data["upcoming_interviews"], list)

def test_dashboard_unauthorized(client):
    """Test dashboard endpoints without authentication"""
    endpoints = [
        "/api/v1/dashboard/summary",
        "/api/v1/dashboard/stats",
        "/api/v1/dashboard/recent-activity",
        "/api/v1/dashboard/upcoming"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401
