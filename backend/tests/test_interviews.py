def test_get_interviews_empty(client, authenticated_user):
    """Test getting interviews when none exist"""
    response = client.get("/api/v1/interviews", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert data["interviews"] == []
    assert data["total"] == 0

def test_create_interview(client, authenticated_user):
    """Test creating a new interview"""
    interview_data = {
        "company_name": "Test Corp",
        "role_title": "Software Engineer",
        "work_mode": "REMOTE",
        "application_status": "APPLIED"
    }
    
    response = client.post("/api/v1/interviews", json=interview_data, headers=authenticated_user)
    assert response.status_code == 201
    
    data = response.json()
    assert data["company_name"] == interview_data["company_name"]
    assert data["role_title"] == interview_data["role_title"]
    assert data["work_mode"] == interview_data["work_mode"]
    assert "id" in data

def test_create_interview_missing_fields(client, authenticated_user):
    """Test creating interview with missing required fields"""
    interview_data = {
        "company_name": "Test Corp"
        # Missing role_title and work_mode
    }
    
    response = client.post("/api/v1/interviews", json=interview_data, headers=authenticated_user)
    assert response.status_code == 422  # Validation error

def test_get_interview_metadata(client):
    """Test getting interview metadata"""
    response = client.get("/api/v1/interviews/metadata")
    assert response.status_code == 200
    
    data = response.json()
    assert "statuses" in data
    assert "work_modes" in data
    assert "currencies" in data

def test_create_interview_unauthorized(client):
    """Test creating interview without authentication"""
    interview_data = {
        "company_name": "Test Corp",
        "role_title": "Software Engineer",
        "work_mode": "REMOTE"
    }
    
    response = client.post("/api/v1/interviews", json=interview_data)
    assert response.status_code == 401

def test_get_interviews_with_data(client, authenticated_user):
    """Test getting interviews after creating some"""
    # Create a few interviews
    for i in range(3):
        interview_data = {
            "company_name": f"Company {i}",
            "role_title": f"Role {i}",
            "work_mode": "REMOTE"
        }
        client.post("/api/v1/interviews", json=interview_data, headers=authenticated_user)
    
    # Get interviews
    response = client.get("/api/v1/interviews", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["interviews"]) == 3
    assert data["total"] == 3
