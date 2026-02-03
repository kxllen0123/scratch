"""
Tests for CodeReviewRequest model validation constraints

This test file contains unit tests for input validation edge cases.
"""


def test_code_field_empty_string_returns_422(client):
    """
    Test that empty code string is rejected with 422

    This test verifies the edge case where the 'code' field is an empty string.
    According to requirement 3.5, when the 'code' field is an empty string,
    the API should return HTTP 422 with an error message.

    Validates: Requirement 3.5
    """
    response = client.post("/api/review", json={"code": "", "language": "python"})
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("code" in str(error).lower() for error in error_detail)


def test_code_field_exceeds_max_length_returns_422(client):
    """
    Test that code exceeding 100,000 characters is rejected with 422

    Validates: Requirement 3.2 (max_length constraint)
    """
    long_code = "x" * 100001  # 100,001 characters
    response = client.post(
        "/api/review", json={"code": long_code, "language": "python"}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("code" in str(error).lower() for error in error_detail)


def test_code_field_at_max_length_is_accepted(client):
    """
    Test that code at exactly 100,000 characters is accepted

    Validates: Requirement 3.2 (boundary condition)
    """
    max_code = "x" * 100000  # Exactly 100,000 characters
    response = client.post("/api/review", json={"code": max_code, "language": "python"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_code_field_missing_returns_422(client):
    """
    Test that missing code field is rejected with 422

    Validates: Requirement 3.2 (required field)
    """
    response = client.post("/api/review", json={"language": "python"})
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("code" in str(error).lower() for error in error_detail)


def test_language_field_defaults_to_python(client):
    """
    Test that language field defaults to 'python' when not provided

    Validates: Requirement 3.3 (default value)
    """
    response = client.post("/api/review", json={"code": "def hello(): pass"})
    assert response.status_code == 200
    data = response.json()
    assert "python" in data["summary"]


def test_valid_request_with_custom_language(client):
    """
    Test that valid request with custom language is accepted

    Validates: Requirement 3.3 (optional language field)
    """
    response = client.post(
        "/api/review", json={"code": "console.log('hello');", "language": "javascript"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "javascript" in data["summary"]


def test_valid_minimal_code(client):
    """
    Test that minimal valid code (1 character) is accepted

    Validates: Requirement 3.2 (min_length boundary)
    """
    response = client.post("/api/review", json={"code": "x", "language": "python"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
