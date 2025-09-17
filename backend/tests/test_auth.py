def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "password" not in data

def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email fails"""
    # First registration
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Second registration with same email
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_user(client, test_user_data):
    """Test user login"""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == test_user_data["email"]

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@email.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, authenticated_user):
    """Test getting current user info"""
    response = client.get("/api/v1/auth/me", headers=authenticated_user)
    assert response.status_code == 200
    
    data = response.json()
    assert "email" in data
    assert "full_name" in data
    assert "id" in data

def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_logout(client, authenticated_user):
    """Test user logout"""
    response = client.post("/api/v1/auth/logout", headers=authenticated_user)
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]
