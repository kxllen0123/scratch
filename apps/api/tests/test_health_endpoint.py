"""
Tests for health check endpoint GET /health

This test file verifies that the health check endpoint returns the correct response:
- Returns HTTP status code 200
- Returns status "healthy"

Validates Requirements: 2.3, 2.4
"""


class TestHealthEndpoint:
    """Tests for the health check endpoint GET /health"""

    def test_health_endpoint_returns_200(self, client):
        """Test that GET /health returns HTTP status code 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self, client):
        """Test that GET /health returns status 'healthy'"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_response_structure(self, client):
        """Test that GET /health returns a JSON object with the expected structure"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1  # Should only have one key
        assert "status" in data
