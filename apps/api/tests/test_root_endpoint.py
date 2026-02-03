"""
Tests for root endpoint GET /

This test file verifies that the root endpoint returns the correct response:
- Returns HTTP status code 200
- Returns message "Code-Sentinel API is running"

Validates Requirements: 2.1, 2.2
"""


class TestRootEndpoint:
    """Tests for the root endpoint GET /"""

    def test_root_endpoint_returns_200(self, client):
        """Test that GET / returns HTTP status code 200"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_correct_message(self, client):
        """Test that GET / returns message 'Code-Sentinel API is running'"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert data["message"] == "Code-Sentinel API is running"

    def test_root_endpoint_response_structure(self, client):
        """Test that GET / returns a JSON object with the expected structure"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1  # Should only have one key
        assert "message" in data
