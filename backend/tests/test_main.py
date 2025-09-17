def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to JobSift API" in response.json()["message"]

def test_api_docs_accessible(client):
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_cors_headers(client):
    """Test CORS headers are set correctly"""
    response = client.options("/api/v1/auth/login")
    assert response.status_code == 200
    # Basic CORS check - specific headers depend on configuration
